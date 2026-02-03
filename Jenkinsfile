pipeline {
    agent any
    
    environment {
        SCANNER_HOME = tool 'SonarQubeScanner'
        SNYK_TOKEN   = credentials('snyk-token')
        DOJO_TOKEN   = credentials('defectdojo-token')
        IMAGE_NAME   = "secure-app:${env.BUILD_NUMBER}"
    }

    stages {
        stage('1. Secret Scan') {
            steps {
                sh "gitleaks detect --source . --verbose --redact"
            }
        }

        stage('2. SAST (SonarQube)') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh "${SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectKey=MyProject"
                }
            }
        }

        stage('3. Dependency Scan (Snyk)') {
            steps {
                sh "snyk test --token=${SNYK_TOKEN} --severity-threshold=high"
            }
        }

        stage('4. Build & Container Scan') {
            steps {
                sh "docker build -t ${IMAGE_NAME} ."
                // Parallel scanning with Trivy and Clair
                sh "trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}"
                // sh "clair-scanner --ip 172.17.0.1 ${IMAGE_NAME}" 
            }
        }

        stage('5. Image Signing (Cosign)') {
            steps {
                // Keyless signing using OIDC
                sh "cosign sign --yes ${IMAGE_NAME}"
            }
        }

        stage('6. IaC & Policy (OPA)') {
            steps {
                // Check K8s manifests against OPA policies
                sh "opa eval --data policy.rego --input k8s/deployment.yaml 'data.main.deny'"
            }
        }

        stage('7. K8s Security Audit') {
            steps {
                sh "kube-bench run --targets master,node"
            }
        }

        stage('8. Dynamic Scan (OWASP ZAP)') {
            steps {
                // Running ZAP in API scan mode against the dev endpoint
                sh "docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-api-scan.py -t http://dev-api:5000/openapi.json -f openapi -r zap_report.html"
            }
        }

        stage('9. Push to DefectDojo') {
            steps {
                // Centralize all findings
                defectDojoPublisher(
                    artifact: 'zap_report.html',
                    productName: 'Secure-Microservices',
                    scanType: 'ZAP Scan',
                    engagementName: "Build-${env.BUILD_NUMBER}"
                )
            }
        }
    }
}
