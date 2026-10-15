#!/bin/bash
set -e
APP_DIR=/home/ubuntu/ml-app

# 1. Install Python tools (first time only)
apt-get update -y
apt-get install -y python3-venv python3-pip
if [ ! -d /opt/ml-venv ]; then
  python3 -m venv /opt/ml-venv
fi

# 2. Install libraries and train the model
cd $APP_DIR
/opt/ml-venv/bin/pip install --no-cache-dir -r requirements.txt
/opt/ml-venv/bin/python train.py

# 3. Free port 80 if Nginx is running from the web page lab
systemctl disable --now nginx 2>/dev/null || true

# 4. Run the app as a service on port 80
cat > /etc/systemd/system/ml-app.service <<SERVICE
[Unit]
Description=Iris ML app
After=network.target

[Service]
WorkingDirectory=$APP_DIR
ExecStart=/opt/ml-venv/bin/gunicorn --bind 0.0.0.0:80 app:app
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable ml-app
systemctl restart ml-app
echo "ML app deployed!"
