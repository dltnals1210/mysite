#!/bin/bash
set -euo pipefail

# ---------------------------
# 환경 변수 기본값 설정
# (Jenkins에서 전달 안 될 경우 대비)
# ---------------------------
PROJECT_DIR=${PROJECT_DIR:-/home/vagrant/mysite}
REPO_URL=${REPO_URL:-https://github.com/dltnals1210/mysite.git}
BRANCH=${BRANCH:-main}
GITHUB_PAT=${GITHUB_PAT:-}

# ---------------------------
# 1) 디렉토리 준비
# ---------------------------
mkdir -p "${PROJECT_DIR}"
cd "${PROJECT_DIR}"

# ---------------------------
# 2) Git Clone or Pull (프라이빗 레포 대응)
# ---------------------------
if [ -n "$GITHUB_PAT" ]; then
    # PAT 인증용 URL 구성
    AUTH_URL="https://x-access-token:${GITHUB_PAT}@${REPO_URL#https://}"
else
    AUTH_URL="$REPO_URL"
fi

if [ ! -d .git ]; then
    echo "[INFO] Repository not found. Cloning..."
    git clone -b "${BRANCH}" "${AUTH_URL}" .
else
    echo "[INFO] Repository exists. Pulling latest changes..."
    git fetch origin "${BRANCH}"
    git reset --hard "origin/${BRANCH}"
fi

# ---------------------------
# 3) 가상환경 준비
# ---------------------------
if [ ! -d venv ]; then
    python3 -m venv venv
fi

source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# ---------------------------
# 4) .env (환경파일) 준비 (선택)
# ---------------------------
# cp /home/vagrant/.env.production .env || true

# ---------------------------
# 5) 장고 명령어
# ---------------------------
python3 manage.py makemigrations --noinput --settings=mysite.settings.local
python3 manage.py migrate --noinput --settings=mysite.settings.local
python3 manage.py collectstatic --noinput --settings=mysite.settings.local

# ---------------------------
# 6) 서버 재시작
# ---------------------------
pkill -f "manage.py runserver" || true
nohup python3 manage.py runserver 0.0.0.0:8000 > /var/log/pybo_run.log 2>&1 &

echo "[INFO] DEPLOY_OK $(date)"

