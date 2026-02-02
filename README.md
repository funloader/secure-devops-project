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
