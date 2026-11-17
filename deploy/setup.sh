#!/bin/bash
# Playsaku one-time VPS setup. Run as root: bash /var/www/playsaku/deploy/setup.sh
set -e
DOMAIN=game.toolsak.online
DIR=/var/www/playsaku
cat > /etc/nginx/sites-available/playsaku <<NGX
server {
    listen 80;
    server_name $DOMAIN;
    root $DIR/dist;
    index index.html;
    location / { try_files \$uri \$uri/ =404; }
    location /assets/ { expires 7d; add_header Cache-Control "public"; }
    location ~ /\. { deny all; }
    gzip on; gzip_types text/css application/javascript image/svg+xml application/xml;
}
NGX
ln -sf /etc/nginx/sites-available/playsaku /etc/nginx/sites-enabled/playsaku
nginx -t && systemctl reload nginx
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --redirect --register-unsafely-without-email || certbot --nginx -d $DOMAIN --redirect
( crontab -l 2>/dev/null | grep -v playsaku ; echo "*/5 * * * * cd $DIR && git pull -q origin main >/dev/null 2>&1 # playsaku" ) | crontab -
echo "PLAYSAKU READY: https://$DOMAIN"
