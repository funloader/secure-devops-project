const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

// 🛡️ SECURITY: Define the secret key
const ADMIN_SECRET = "SuperSecretAdminKey123";

// Current state (in-memory)
let orderStore = {
    order_id: "ORD-101",
    status: "Shipped",
    customer: "funloader"
};

// GET endpoint
app.get('/order', (req, res) => {
    res.json(orderStore);
});

// 🛡️ SECURE PATCH: Now checks for the 'x-admin-key' header
app.patch('/order/status', (req, res) => {
    const userKey = req.headers['x-admin-key'];
    const { newStatus } = req.body;

    // 1. Check Authorization
    if (userKey !== ADMIN_SECRET) {
        return res.status(403).json({ 
            error: "Forbidden", 
            message: "Invalid or missing Admin Key." 
        });
    }

    // 2. Update Status if valid
    if (newStatus) {
        orderStore.status = newStatus;
        return res.json({ message: "Status updated by Admin!", current: orderStore });
    }
    
    res.status(400).json({ error: "Invalid status" });
});

app.listen(5002, () => console.log('Order API running on 5002'));