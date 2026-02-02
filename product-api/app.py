from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('products.db')
    # 🛡️ Added 'category' and 'price' columns
    conn.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER, name TEXT, category TEXT, price REAL)')
    conn.execute('DELETE FROM products')
    
    # Extended Inventory Data
    inventory = [
        (1, "MacBook Pro", "Electronics", 2400.00),
        (2, "iPhone 15", "Electronics", 999.00),
        (3, "Mechanical Keyboard", "Accessories", 150.00),
        (4, "Ergonomic Chair", "Furniture", 350.00),
        (5, "Monitor 4K", "Electronics", 500.00)
    ]
    conn.executemany('INSERT INTO products VALUES (?,?,?,?)', inventory)
    conn.commit()
    conn.close()

# --- THE VULNERABLE ENDPOINT (For ZAP/Trivy to find) ---
@app.route('/product')
def get_product():
    product_id = request.args.get('id')
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    # DANGEROUS: String formatting (SQLi Vulnerability)
    query = f"SELECT name, price FROM products WHERE id = {product_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return {"product": result[0], "price": result[1]} if result else {"error": "Not Found"}

# --- THE NEW EXTENDED ENDPOINT (Securely Parameterized) ---
@app.route('/products/category/<cat_name>')
def get_by_category(cat_name):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    # 🛡️ SECURE: Using '?' placeholder prevents SQL injection
    query = "SELECT name, price FROM products WHERE category = ?"
    cursor.execute(query, (cat_name,))
    results = cursor.fetchall()
    conn.close()
    return jsonify({"items": [{"name": r[0], "price": r[1]} for r in results]})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001)