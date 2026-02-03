pipeline {
    agent any
    
    environment {
        // Define our SonarQube Server (must match Name in Jenkins Tools)
        SONAR_SERVER = 'SonarQube'
        SCANNER_HOME = tool 'SonarQubeScanner'
        APP_NAME     = "secure-product-api"
    }

    stages {
        stage('Step 1: Cleanup') {
            steps {
                echo 'Cleaning up workspace...'
                deleteDir()
                checkout scm
            }
        }

        stage('Step 2: Secret Scanning (Gitleaks)') {
            steps {
                echo 'Running Gitleaks...'
                // Running via Docker container to avoid local installation
                sh "docker run --rm -v ${WORKSPACE}:/path zricethezav/gitleaks:latest detect --source=/path --verbose"
            }
        }

        stage('Step 3: SCA & Code Quality (SonarQube)') {
            steps {
                echo 'Analyzing Code Quality...'
                withSonarQubeEnv("${SONAR_SERVER}") {
                    sh "${SCANNER_HOME}/bin/sonar-scanner \
                    -Dsonar.projectKey=Secure-Microservices-Pipeline \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://sonarqube:9000"
                }
            }
        }

        stage('Step 4: Vulnerability Scanning (Trivy)') {
            steps {
                echo 'Scanning Repository for Vulnerabilities...'
                sh "trivy fs . --severity HIGH,CRITICAL"
            }
        }

        stage('Step 5: Build & Image Security') {
            steps {
                echo 'Building Secure Docker Image...'
                sh "docker build -t ${APP_NAME}:${BUILD_NUMBER} ./product-api"
                echo 'Scanning Docker Image...'
                sh "trivy image --severity HIGH,CRITICAL ${APP_NAME}:${BUILD_NUMBER}"
            }
        }

        stage('Step 6: Deploy to K8s (Minikube/Docker Desktop)') {
            steps {
                echo 'Deploying to Local Kubernetes...'
                // This assumes you have your K8s manifests in a folder named /k8s
                sh "kubectl apply -f k8s/"
            }
        }
    }

    post {
        always {
            echo 'Pipeline Execution Finished.'
        }
        success {
            echo 'Security Gates Passed! Deployment Successful.'
        }
        failure {
            echo 'Security Gate Violation Found. Build Aborted.'
        }
    }
}
