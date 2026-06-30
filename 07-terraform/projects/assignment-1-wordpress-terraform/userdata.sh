#!/bin/bash
# ============================================================
# WordPress User Data Script – Ubuntu EC2
# LAMP Stack: Linux + Apache + MySQL + PHP
# ============================================================

# --- 1. Update the system ---
apt-get update -y
apt-get upgrade -y

# --- 2. Install Apache web server ---
apt-get install -y apache2
systemctl start apache2
systemctl enable apache2

# --- 3. Install MySQL server ---
apt-get install -y mysql-server
systemctl start mysql
systemctl enable mysql

# --- 4. Install PHP and required extensions for WordPress ---
apt-get install -y \
  php \
  php-mysql \
  php-curl \
  php-gd \
  php-xml \
  php-mbstring \
  php-xmlrpc \
  php-zip \
  libapache2-mod-php

# --- 5. Create the WordPress database and user ---
# These credentials are referenced again in wp-config.php below
DB_NAME="wordpress"
DB_USER="wp_user"
DB_PASSWORD="StrongPass123!"

mysql -u root <<EOF
CREATE DATABASE IF NOT EXISTS ${DB_NAME};
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
FLUSH PRIVILEGES;
EOF

# --- 6. Download and extract WordPress ---
cd /tmp
wget -q https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz

# --- 7. Move WordPress files to Apache web root ---
cp -r wordpress/* /var/www/html/
# Remove the default Apache placeholder page
rm -f /var/www/html/index.html

# --- 8. Set correct file permissions ---
chown -R www-data:www-data /var/www/html/
chmod -R 755 /var/www/html/

# --- 9. Configure wp-config.php from the sample file ---
cp /var/www/html/wp-config-sample.php /var/www/html/wp-config.php

# Replace placeholder values with the actual DB credentials
sed -i "s/database_name_here/${DB_NAME}/"   /var/www/html/wp-config.php
sed -i "s/username_here/${DB_USER}/"        /var/www/html/wp-config.php
sed -i "s/password_here/${DB_PASSWORD}/"    /var/www/html/wp-config.php

# --- 10. Hardcoding the domain directly into the script so it works on startup  ---
sed -i "s|<?php|<?php\ndefine('WP_HOME','http://wordpress.aws.biram.uk');\ndefine('WP_SITEURL','http://wordpress.aws.biram.uk');|" /var/www/html/wp-config.php

# --- 11. Enable Apache mod_rewrite (needed for WordPress permalinks) ---
a2enmod rewrite

# Allow .htaccess overrides in the web root
sed -i 's/AllowOverride None/AllowOverride All/' /etc/apache2/apache2.conf

# --- 12. Restart Apache to apply all changes ---
systemctl restart apache2