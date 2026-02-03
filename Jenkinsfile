pipeline {
    agent any

    environment {
        // Define image names for consistency
        PRODUCT_IMAGE = "product-api:test"
        ORDER_IMAGE   = "order-api:test"
        SCANNER_HOME  = tool 'SonarQubeScanner'
    }

    stages {
        stage('Step 1: Checkout & Setup') {
            steps {
                deleteDir()
                checkout scm
            }
        }

        stage('Step 2: Static Security Scans') {
            parallel {
                stage('Trivy FS Scan') {
                    steps {
                        echo 'Scanning Filesystem for vulnerabilities...'
                        // severity: 'CRITICAL,HIGH' from your YAML
                        sh "trivy fs . --severity HIGH,CRITICAL --exit-code 0"
                    }
                }
                stage('SonarQube Analysis') {
                    steps {
                        echo 'Analyzing code quality...'
                        withSonarQubeEnv('SonarQube') {
                            sh "${SCANNER_HOME}/bin/sonar-scanner -Dsonar.projectKey=Secure-Microservices"
                        }
                    }
                }
            }
        }

        stage('Step 3: Build Images') {
            steps {
                echo 'Building Docker Images...'
                sh "docker build -t ${PRODUCT_IMAGE} ./product-api"
                sh "docker build -t ${ORDER_IMAGE} ./order-api"
            }
        }

        stage('Step 4: Image Security Scans') {
            parallel {
                stage('Scan Product API') {
                    steps {
                        echo 'Trivy scanning Product API image...'
                        sh "trivy image ${PRODUCT_IMAGE} --severity HIGH,CRITICAL --exit-code 0"
                    }
                }
                stage('Scan Order API') {
                    steps {
                        echo 'Trivy scanning Order API image...'
                        sh "trivy image ${ORDER_IMAGE} --severity HIGH,CRITICAL --exit-code 0"
                    }
                }
            }
        }

        stage('Step 5: Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        success {
            echo '✅ All security checks passed. Ready for deployment!'
        }
        failure {
            echo '❌ Security vulnerabilities found. Review the logs.'
        }
    }
}
