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
    stage('Run Remote Deploy (debug)') {
        steps {
            withCredentials([string(credentialsId: 'github-pat', variable: 'GITHUB_PAT')]) {
                sshagent (credentials: [env.SSH_CRED_ID]) {
                    sh """
                        set -euxo pipefail
                        echo "== Jenkins env =="
                        env | sort | sed -n '1,15p'

                        echo "== Test SSH connectivity =="
                        ssh -vvv -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} 'echo connected: \$(hostname) as \$(whoami)'

                        echo "== Push script via scp =="
                        scp -v -o StrictHostKeyChecking=no scripts/deploy_remote.sh ${DEPLOY_USER}@${DEPLOY_HOST}:/tmp/deploy_remote.sh

                        echo "== Run on remote =="
                        ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} 'bash -s' <<EOF
set -euxo pipefail
echo "remote whoami: \$(whoami)"
echo "remote which bash: \$(which bash)"
echo "remote git version: \$(git --version || echo no-git)"

DEPLOY_DIR="${DEPLOY_DIR}"
REPO_URL="${REPO_URL}"
BRANCH="${BRANCH}"

echo "DEPLOY_DIR=\\${DEPLOY_DIR}  REPO_URL=\\${REPO_URL}  BRANCH=\\${BRANCH}"
mkdir -p "\\${DEPLOY_DIR}"

head -n1 /tmp/deploy_remote.sh || true
chmod +x /tmp/deploy_remote.sh
/tmp/deploy_remote.sh
echo "script exit code: \\$?"
EOF
                    """
                }
            }
        }
    }

  }

  post {
    success { echo "Deployment succeeded" }
    failure { echo "Deployment failed" }
  }
}

