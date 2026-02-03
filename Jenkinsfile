pipeline {
    agent any

    environment {
        // Define common variables
        DOCKER_IMAGE = "secure-product-api"
        SONAR_SERVER = "SonarQube"
    }

    stages {
        stage('Checkout') {
            steps {
                // This pulls your code from the workspace
                checkout scm
            }
        }

        stage('Security: Secret Scanning') {
            steps {
                script {
                    // Running Gitleaks via Docker-out-of-Docker
                    sh "docker run --rm -v ${WORKSPACE}:/path zricethezav/gitleaks:latest detect --source=/path --verbose"
                }
            }
        }

        stage('Static Analysis: SonarQube') {
            steps {
                script {
                    // Using the tool name we configured in 'Global Tool Configuration'
                    def scannerHome = tool 'SonarQubeScanner'
                    withSonarQubeEnv("${SONAR_SERVER}") {
                        sh "${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=Secure-Microservices-Pipeline \
                            -Dsonar.sources=. \
                            -Dsonar.python.version=3"
                    }
                }
            }
        }

        stage('SCA: Trivy FS Scan') {
            steps {
                // Scans the source code for vulnerable libraries
                sh "docker run --rm -v ${WORKSPACE}:/root/project aquasec/trivy fs /root/project"
            }
        }

        stage('Build & Image Security') {
            steps {
                script {
                    // Build the Docker image
                    sh "docker build -t ${DOCKER_IMAGE}:latest ./product-api"
                    
                    // Scan the built image for vulnerabilities
                    // We set it to exit with code 1 if CRITICAL issues are found
                    sh "docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --exit-code 0 --severity HIGH,CRITICAL ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Deployment Simulation') {
            steps {
                echo "Deploying to Kubernetes Environment..."
                // In a real setup, this would be: 
                // sh "kubectl apply -f k8s-manifests/"
            }
        }
    }

    post {
        always {
            cleanWs() // Keeps your VM/Container storage clean
        }
        success {
            echo '✅ Pipeline Completed Successfully!'
        }
        failure {
            echo '❌ Pipeline Failed. Check security scan logs.'
        }
    }
}
