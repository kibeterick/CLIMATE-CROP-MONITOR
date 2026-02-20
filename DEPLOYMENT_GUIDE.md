# Climate Crop Monitor - Deployment Guide

## Deployment Options

### Option 1: Local Development (Current Setup)
Already configured - see INSTALLATION.md

### Option 2: Production Deployment

## Pre-Deployment Checklist

- [ ] All tests passing (see TESTING_GUIDE.md)
- [ ] Database migrations up to date
- [ ] Static files collected
- [ ] Environment variables configured
- [ ] API keys obtained
- [ ] Security settings reviewed
- [ ] Backup strategy in place

## Production Environment Setup

### 1. Server Requirements

**Minimum Specifications:**
- OS: Ubuntu 20.04 LTS or Windows Server 2019
- RAM: 2GB
- Storage: 10GB
- Python: 3.8+
- Database: PostgreSQL 12+

**Recommended Specifications:**
- OS: Ubuntu 22.04 LTS
- RAM: 4GB
- Storage: 20GB
- Python: 3.10+
- Database: PostgreSQL 14+

### 2. Install Dependencies (Ubuntu)

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3.10 python3-pip python3-venv -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Nginx (web server)
sudo apt install nginx -y

# Install supervisor (process manager)
sudo apt install supervisor -y
```

### 3. Database Setup (PostgreSQL)

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE ccm_db;
CREATE USER ccm_user WITH PASSWORD 'your_secure_password';
ALTER ROLE ccm_user SET client_encoding TO 'utf8';
ALTER ROLE ccm_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ccm_user SET timezone TO 'Africa/Nairobi';
GRANT ALL PRIVILEGES ON DATABASE ccm_db TO ccm_user;
\q
```

### 4. Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/ccm
cd /var/www/ccm

# Clone or upload your project
# (Upload your project files here)

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Create .env file
nano .env
```

### 5. Environment Configuration (.env)

```env
# Production settings
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip

# Database
DATABASE_NAME=ccm_db
DATABASE_USER=ccm_user
DATABASE_PASSWORD=your_secure_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# API Keys
OPENWEATHER_API_KEY=your-api-key-here

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

### 6. Update Django Settings for Production

Edit `ccm_project/settings.py`:

```python
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 7. Collect Static Files and Migrate

```bash
# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 8. Configure Gunicorn

Create `/var/www/ccm/gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
loglevel = "info"
```

Create log directory:
```bash
sudo mkdir -p /var/log/gunicorn
sudo chown -R www-data:www-data /var/log/gunicorn
```

### 9. Configure Supervisor

Create `/etc/supervisor/conf.d/ccm.conf`:

```ini
[program:ccm]
directory=/var/www/ccm
command=/var/www/ccm/venv/bin/gunicorn ccm_project.wsgi:application -c /var/www/ccm/gunicorn_config.py
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/ccm.log
```

Start supervisor:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start ccm
```

### 10. Configure Nginx

Create `/etc/nginx/sites-available/ccm`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 10M;

    location /static/ {
        alias /var/www/ccm/staticfiles/;
    }

    location /media/ {
        alias /var/www/ccm/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/ccm /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 11. SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
```

### 12. Firewall Configuration

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## Deployment to Cloud Platforms

### Heroku Deployment

1. **Install Heroku CLI**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Create Heroku App**
```bash
heroku login
heroku create ccm-app-name
```

3. **Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Configure Environment Variables**
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set OPENWEATHER_API_KEY=your-api-key
heroku config:set DEBUG=False
```

5. **Create Procfile**
```
web: gunicorn ccm_project.wsgi --log-file -
```

6. **Deploy**
```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### AWS EC2 Deployment

Follow the Ubuntu production setup above on an EC2 instance.

**Additional Steps:**
1. Create EC2 instance (Ubuntu 22.04)
2. Configure security groups (ports 22, 80, 443)
3. Allocate Elastic IP
4. Follow production setup steps
5. Configure Route 53 for domain

### DigitalOcean Deployment

Similar to AWS EC2:
1. Create Droplet (Ubuntu 22.04)
2. Follow production setup steps
3. Configure domain in DigitalOcean DNS

## Post-Deployment Tasks

### 1. Verify Deployment

```bash
# Check application status
sudo supervisorctl status ccm

# Check Nginx status
sudo systemctl status nginx

# Check logs
sudo tail -f /var/log/supervisor/ccm.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Test Application

- [ ] Access homepage
- [ ] Test user registration
- [ ] Test login
- [ ] Create farm
- [ ] Register crop
- [ ] Update weather
- [ ] Check predictions
- [ ] Test alerts

### 3. Setup Monitoring

**Install monitoring tools:**
```bash
# Install htop for system monitoring
sudo apt install htop -y

# Install fail2ban for security
sudo apt install fail2ban -y
```

### 4. Setup Backups

**Database Backup Script** (`/var/www/ccm/backup.sh`):
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/ccm"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U ccm_user ccm_db > $BACKUP_DIR/db_$DATE.sql

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/ccm/media/

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
```

**Setup cron job:**
```bash
sudo crontab -e
# Add: 0 2 * * * /var/www/ccm/backup.sh
```

### 5. Setup Log Rotation

Create `/etc/logrotate.d/ccm`:
```
/var/log/gunicorn/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

## Maintenance

### Update Application

```bash
cd /var/www/ccm
source venv/bin/activate

# Pull latest changes
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application
sudo supervisorctl restart ccm
```

### Database Maintenance

```bash
# Vacuum database
sudo -u postgres psql ccm_db -c "VACUUM ANALYZE;"

# Check database size
sudo -u postgres psql ccm_db -c "SELECT pg_size_pretty(pg_database_size('ccm_db'));"
```

## Troubleshooting

### Application Won't Start
```bash
# Check logs
sudo tail -f /var/log/supervisor/ccm.log

# Check permissions
sudo chown -R www-data:www-data /var/www/ccm

# Restart services
sudo supervisorctl restart ccm
```

### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
sudo -u postgres psql -c "\l"
```

### Static Files Not Loading
```bash
# Recollect static files
python manage.py collectstatic --noinput

# Check Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

## Security Best Practices

1. **Keep system updated**
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Use strong passwords**
- Database passwords
- Admin passwords
- Secret keys

3. **Enable firewall**
```bash
sudo ufw enable
```

4. **Regular backups**
- Daily database backups
- Weekly full backups

5. **Monitor logs**
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/supervisor/ccm.log
```

6. **SSL/TLS enabled**
- Use Let's Encrypt certificates
- Auto-renewal configured

## Performance Optimization

### 1. Database Indexing
Already configured in models

### 2. Caching (Optional)
Install Redis:
```bash
sudo apt install redis-server -y
pip install django-redis
```

### 3. CDN for Static Files (Optional)
Use AWS CloudFront or Cloudflare

### 4. Database Connection Pooling
Install pgbouncer for better performance

## Monitoring and Analytics

### Setup Application Monitoring
- Use Sentry for error tracking
- Use New Relic for performance monitoring
- Use Google Analytics for user analytics

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Multiple application servers
- Shared database server
- Shared media storage (S3)

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Add caching layer

## Support

For deployment issues:
- Developer: ARON SIGEI
- Institution: Kisii University
- Department: Department of Computing

---

**Deployment Status**: Ready for Production  
**Last Updated**: February 2026  
**Version**: 1.0
