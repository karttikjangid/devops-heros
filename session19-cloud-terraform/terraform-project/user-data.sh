#!/bin/bash
set -eu
dnf install -y httpd
printf '<h1>Session 19: Cloud &amp; Terraform</h1><p>Kartik | EC2 provisioned with Terraform.</p>\n' > /var/www/html/index.html
systemctl enable --now httpd
