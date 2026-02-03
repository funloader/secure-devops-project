pipeline {
    agent any
    
    environment {
        SONAR_SERVER = 'SonarQube'
        SCANNER_HOME = tool 'SonarQubeScanner'
        APP_NAME     = "secure-product-api"
    }

    stages {
        stage('Step 1: Checkout') {
            steps {
                deleteDir()
                checkout scm
            }
        }

        /* stage('Step 2: Secret Scanning (Gitleaks)') {
            steps {
                echo 'Skipping Gitleaks for this run...'
            }
        } 
        */

        stage('Step 2: Code Quality (SonarQube)') {
            steps {
                script {
                    withSonarQubeEnv("${SONAR_SERVER}") {
                        sh "${SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=Secure-Microservices-Pipeline \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://sonarqube:9000"
                    }
                }
            }
        }

        stage("Step 3: Sonar Quality Gate") {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    // This waits for SonarQube to finish analysis and return a Pass/Fail
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Step 4: Vulnerability Scanning (Trivy)') {
            steps {
                sh "trivy fs . --severity HIGH,CRITICAL"
            }
        }

        stage('Step 5: Build & Image Security') {
            steps {
                sh "docker build -t ${APP_NAME}:latest ./product-api"
                sh "trivy image --severity HIGH,CRITICAL ${APP_NAME}:latest"
            }
        }

        stage('Step 6: Deploy to K8s') {
            steps {
                // Ensure the 'k8s' folder exists with your yaml files
                sh "kubectl apply -f k8s/"
            }
        }
    }
}
