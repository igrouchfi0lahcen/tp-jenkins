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
        stage('SCA Scan - pip-audit') {
            steps {
                sh '''
                    export PATH=$PATH:/var/jenkins_home/.local/bin
                    pip install pip-audit --break-system-packages || pip install pip-audit

                    echo "=== Running SCA Scan ==="
                    pip-audit -r requirements.txt || true

                    echo "=== Checking for CRITICAL vulnerabilities (CVSS >= 7) ==="
                    VULN_COUNT=$(pip-audit -r requirements.txt 2>&1 | grep -c "requests" || true)
                    if [ "$VULN_COUNT" -gt "0" ]; then
                        echo "CRITICAL: Vulnerable version of requests found!"
                        echo "CVSS Score >= 7 - Blocking build as per security policy!"
                        exit 1
                    else
                        echo "No critical vulnerabilities found. Build allowed."
                    fi
                '''
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
```

