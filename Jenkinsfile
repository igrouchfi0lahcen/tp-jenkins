pipeline {
    agent any

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

        stage('SAST Scan - Bandit') {
            steps {
                sh '''
                    pip install bandit --break-system-packages || pip install bandit
                     export PATH=$PATH:/var/jenkins_home/.local/bin
                    bandit -r app.py -f txt -o bandit_report.txt || true
                    cat bandit_report.txt
                '''
            }
        }

        stage('SCA Scan - OWASP Dependency Check') {
            steps {
                 sh '''
            export PATH=$PATH:/var/jenkins_home/.local/bin
            pip install pip-audit --break-system-packages || pip install pip-audit
            export PATH=$PATH:/var/jenkins_home/.local/bin
            pip-audit -r requirements.txt -f json -o sca_report.json || true
            pip-audit -r requirements.txt || true
        '''
            }
            // post {
            //     always {
            //         dependencyCheckPublisher pattern: 'dependency-check-report/dependency-check-report.xml'
            //     }
            // }
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
