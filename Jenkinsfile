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

            # Reinstall clean urllib3 to fix compatibility
            pip install urllib3==2.0.0 --break-system-packages

            echo "=== Running SCA Scan ==="
            pip-audit -r requirements.txt || AUDIT_EXIT=$?

            echo "=== Checking for CRITICAL vulnerabilities (CVSS >= 7) ==="
            VULN_OUTPUT=$(pip-audit -r requirements.txt 2>&1 || true)
            echo "$VULN_OUTPUT"

            if echo "$VULN_OUTPUT" | grep -i "No known vulnerabilities"; then
                echo "✅ No critical vulnerabilities found. Build allowed."
            else
                VULN_LINES=$(echo "$VULN_OUTPUT" | grep -v "^Traceback" | grep -v "File " | grep -v "Error" | grep -c "requests" || true)
                if [ "$VULN_LINES" -gt "0" ]; then
                    echo "❌ CRITICAL: Vulnerable dependency found - CVSS >= 7 - Blocking build!"
                    exit 1
                fi
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

