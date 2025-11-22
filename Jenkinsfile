pipeline {
    agent any

    environment {
        PATH = "/opt/homebrew/bin:/usr/local/bin:${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Safety Check') {
            steps {
                script {
                    if (fileExists('.github/workflows')) {
                        error "❌ GitHub Actions workflows detected! They must be removed to avoid cost/security risks."
                    }
                }
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Running tests...'
                // Detect project type and run appropriate tests
                script {
                    if (fileExists('package.json')) {
                        sh 'npm install && npm test'
                    } else if (fileExists('requirements.txt')) {
                        sh 'pip install -r requirements.txt && pytest'
                    } else {
                        echo '⚠️ Unknown project type, skipping tests'
                    }
                }
            }
        }
    }
}
