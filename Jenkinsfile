pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/YOUR_USERNAME/tp-jenkins.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt --break-system-packages || pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python -m pytest test_app.py -v'
            }
        }

        stage('SAST Scan - Bandit') {
            steps {
                sh '''
                    pip install bandit --break-system-packages || pip install bandit
                    bandit -r app.py -f txt -o bandit_report.txt || true
                    cat bandit_report.txt
                '''
            }
        }

        stage('SCA Scan - OWASP Dependency Check') {
            steps {
                dependencyCheck additionalArguments: '--scan . --format HTML --out dependency-check-report', odcInstallation: 'OWASP-DC'
            }
            post {
                always {
                    dependencyCheckPublisher pattern: 'dependency-check-report/dependency-check-report.xml'
                }
            }
        }

    }

    post {
        failure {
            echo 'Build failed due to errors or vulnerabilities!'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
    }
}
