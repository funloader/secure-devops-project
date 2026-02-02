### 🚀 End to End Secure Microservices Pipeline

A hands-on DevSecOps implementation focusing on shifting security left.

#### 🛠 Tech Stack

* **Infrastructure:** Docker, Docker-Compose, Kubernetes (Minikube).
* **CI/CD:** GitHub Actions.
* **Security Tools:** * **SCA:** Trivy (Filesystem & Image)
* **SAST:** Gitleaks, SonarQube
* **DAST:** OWASP ZAP
* **Compliance:** Kube-bench (CIS Benchmarks)
* **Policy-as-Code:** OPA (Open Policy Agent)

#### 🛡 Security Milestones

1. **Secrets Management:** Identified hardcoded AWS keys using **Gitleaks**; implemented conceptual remediation via **HashiCorp Vault**.
2. **Vulnerability Management:** Discovered 40+ Critical CVEs in legacy base images using **Trivy**; optimized Dockerfiles for security.
3. **Cluster Auditing:** Performed automated audits of K8s nodes using **Kube-bench** to ensure CIS compliance.
4. **Runtime Analysis:** Conducted automated **DAST** scans using **OWASP ZAP** to identify missing security headers and version disclosure.

A comprehensive **DevSecOps** laboratory demonstrating a "Shift Left" security strategy. This project features a microservices architecture, automated security scanning, and demonstrated vulnerability remediation.

## 🏗️ Architecture
* **Frontend-1**: Hardened Nginx Reverse Proxy (Alpine-based).
* **Product API**: Python/Flask service (Remediated from SQLi).
* **Order API**: Node.js service (Monitored for Secrets).

## 🛡️ Security Implementation & Remediation

### 1. Web Security & Hardening (Nginx)
* **Finding**: Default Nginx exposed version numbers and lacked security headers.
* **Remediation**: Implemented `server_tokens off;` and added `X-Frame-Options`, `X-Content-Type-Options`, and `CSP` headers.

### 2. SQL Injection Remediation (Product API)
* **Finding**: The `/product` endpoint was vulnerable to Boolean and Union-based SQLi via string formatting.
* **Attack Vector**: `1 OR 1=1` was used to bypass logic.
* **Remediation**: Transitioned from f-strings to **Parameterized Queries** (`?` placeholders), treating user input strictly as data.

### 3. Pipeline Tooling
* **SAST**: Gitleaks (Secrets), SonarQube (Code Quality).
* **SCA**: Trivy (Dependencies & Images).
* **DAST**: OWASP ZAP (Dynamic Scan).
* **IaC**: Checkov (K8s Manifests).

---

## 🔍 Security Disclosure & Mitigation Report

This project serves as a case study in identifying and remediating common web vulnerabilities (OWASP Top 10). Below are the specific findings and the technical steps taken to secure the environment.

### 1. SQL Injection (SQLi) - [OWASP A03:2021]

* **Vulnerability:** The `product-api` was using Python f-strings to build SQL queries, allowing an attacker to manipulate the database logic via the `id` parameter.
* **Proof of Concept (PoC):** An attacker could use `0 UNION SELECT sqlite_version(), 0` to leak database metadata.
* **Mitigation:** Implemented **Parameterized Queries**. By using the `?` placeholder in `sqlite3`, the database driver now treats all user input as literal data rather than executable code.

### 2. Broken Access Control - [OWASP A01:2021]

* **Vulnerability:** The `order-api` contained an insecure `PATCH` endpoint that allowed any unauthenticated user to change an order's status from `Shipped` to `Delivered`.
* **Proof of Concept (PoC):** A simple `Invoke-RestMethod` without headers was able to manipulate the business logic.
* **Mitigation:** Implemented **Header-based Authorization**. The endpoint now requires a valid `x-admin-key` in the request header, returning a `403 Forbidden` for unauthorized attempts.

### 3. Security Misconfiguration & Info Disclosure - [OWASP A05:2021]

* **Vulnerability:** The Nginx frontend was broadcasting its specific version number in HTTP response headers, assisting attackers in version-specific exploit research.
* **Mitigation:** * Hardened `nginx.conf` with `server_tokens off;`.
* Added security headers: `X-Frame-Options` (Clickjacking protection) and `X-Content-Type-Options` (MIME-sniffing protection).

### 4. Supply Chain & Container Security

* **Vulnerability:** Initial scans showed **40+ High/Critical CVEs** and containers running as `root`.
* **Mitigation:** * Migrated to **Alpine Linux** base images to reduce the attack surface.
* Implemented `USER` directives in Dockerfiles to ensure the application runs with **Least Privilege**.

---
