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
            withCredentials([string(credentialsId: 'github-pat', variable: 'GITHUB_PAT')]) {
                sshagent (credentials: [env.SSH_CRED_ID]) {
                    sh '''
                        set -e
                        ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} "
                            mkdir -p ${DEPLOY_DIR}
                            curl -H 'Authorization: token ${GITHUB_PAT}' -fsSL \
                                 https://raw.githubusercontent.com/dltnals1210/mysite/${BRANCH}/scripts/deploy_remote.sh \
                                 -o /tmp/deploy_remote.sh &&
                            chmod +x /tmp/deploy_remote.sh &&
                            /tmp/deploy_remote.sh
                        "
                    '''
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

