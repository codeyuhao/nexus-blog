#!/usr/bin/env bash
set -e

echo "========================================="
echo "  Nexus Blog - VPS Deployment Script"
echo "========================================="

PROJECT_DIR="/opt/nexus-blog"
DOMAIN_OR_IP="${1:-localhost}"

echo ""
echo "[1/8] Installing system dependencies..."
sudo apt update -y
sudo apt install -y python3 python3-venv python3-pip nginx git curl

echo ""
echo "[2/8] Installing Node.js 20.x..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt install -y nodejs
fi
echo "Node: $(node --version)"
echo "NPM: $(npm --version)"

echo ""
echo "[3/8] Cloning repository..."
sudo rm -rf "$PROJECT_DIR"
sudo git clone https://github.com/codeyuhao/nexus-blog.git "$PROJECT_DIR"
sudo chown -R $USER:$USER "$PROJECT_DIR"

echo ""
echo "[4/8] Setting up Python virtual environment..."
cd "$PROJECT_DIR/backend"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "[5/8] Configuring Django..."
export DEBUG=False
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
export CSRF_TRUSTED_ORIGINS="http://${DOMAIN_OR_IP},https://${DOMAIN_OR_IP}"

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py seed_data

echo ""
echo "[6/8] Building frontend..."
cd "$PROJECT_DIR/frontend"
npm install
npm run build
sudo mkdir -p /var/www/nexus-blog-frontend
sudo cp -r dist/* /var/www/nexus-blog-frontend/
sudo chown -R www-data:www-data /var/www/nexus-blog-frontend

echo ""
echo "[7/8] Configuring services..."
cd "$PROJECT_DIR"

# Create log dir
sudo mkdir -p /var/log/nexus-blog
sudo chown -R www-data:www-data /var/log/nexus-blog

# Setup systemd service
sudo cp deploy/nexus-blog.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable nexus-blog
sudo systemctl restart nexus-blog

# Setup Nginx
sudo cp deploy/nginx.conf /etc/nginx/sites-available/nexus-blog
sudo ln -sf /etc/nginx/sites-available/nexus-blog /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Set permissions
sudo chown -R www-data:www-data "$PROJECT_DIR/backend/staticfiles"
sudo chown -R www-data:www-data "$PROJECT_DIR/backend/media"

echo ""
echo "[8/8] Saving environment variables..."
sudo tee /etc/nexus-blog.env > /dev/null << EOF
DEBUG=False
SECRET_KEY=${SECRET_KEY}
CSRF_TRUSTED_ORIGINS=http://${DOMAIN_OR_IP},https://${DOMAIN_OR_IP}
EOF

sudo chmod 600 /etc/nexus-blog.env

echo ""
echo "========================================="
echo "  Deployment Complete!"
echo "========================================="
echo ""
echo "Your blog is now available at:"
echo "  http://${DOMAIN_OR_IP}"
echo ""
echo "Admin panel:"
echo "  http://${DOMAIN_OR_IP}/admin/"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Manage the service:"
echo "  sudo systemctl status nexus-blog"
echo "  sudo systemctl restart nexus-blog"
echo "  sudo journalctl -u nexus-blog -f"
echo ""