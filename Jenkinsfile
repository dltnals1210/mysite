pipeline {
  agent any

  environment {
    DEPLOY_USER = 'vagrant'
    DEPLOY_HOST = '192.168.56.23'
    DEPLOY_DIR  = '/home/vagrant/mysite'
    REPO_URL    = 'https://github.com/dltnals1210/mysite.git'
    BRANCH      = 'main'
    SSH_CRED_ID = 'deploy-ssh-key'   // Jenkins에 만든 credentials ID
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Run Remote Deploy') {
        steps {
            sshagent (credentials: [SSH_CRED_ID]) {
                sh """
                    scp -o StrictHostKeyChecking=no scripts/deploy_remote.sh ${DEPLOY_USER}@${DEPLOY_HOST}:/tmp/deploy_remote.sh
                    ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} 'bash -s' <<'EOF'
set -euo pipefail
chmod +x /tmp/deploy_remote.sh
bash /tmp/deploy_remote.sh
EOF
                """
            }
        }
    }

  }

  post {
    success { echo "Deployment succeeded" }
    failure { echo "Deployment failed" }
  }
}

