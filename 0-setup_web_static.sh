#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Install Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx

# Create required directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file to test Nginx configuration
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link (force recreate if it exists)
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve /data/web_static/current/ at /hbnb_static
nginx_config="/etc/nginx/sites-available/default"
if ! grep -q "location /hbnb_static" "$nginx_config"; then
    sudo sed -i '/server_name _;/a \    location /hbnb_static {\n        alias /data/web_static/current/;\n    }' "$nginx_config"
fi

# Restart Nginx
sudo service nginx restart

exit 0
