pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonarqube-token')
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/igrouchfi0lahcen/tp-jenkins'
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

        stage('SAST Scan - SonarQube') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        export PATH=$PATH:/var/jenkins_home/.local/bin
                        sonar-scanner \
                          -Dsonar.projectKey=TP-Jenkins \
                          -Dsonar.sources=. \
                          -Dsonar.host.url=http://sonarqube:9000 \
                          -Dsonar.token=${SONAR_TOKEN}
                    '''
                }
            }
        }

        stage('SCA Scan - OWASP Dependency Check') {
            steps {
                dependencyCheck additionalArguments: '''
                    --project "TP-Jenkins"
                    --scan .
                    --format HTML
                    --format XML
                    --out dependency-check-report
                ''', odcInstallation: 'OWASP-DC'
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
