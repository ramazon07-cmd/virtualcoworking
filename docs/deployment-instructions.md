# VirtualCoworking Production Deployment Instructions

## Prerequisites

1. A Linux server (Ubuntu 20.04 LTS recommended)
2. Docker and Docker Compose installed
3. Domain name configured with DNS records
4. SSL certificates (Let's Encrypt or commercial)
5. SMTP credentials for email sending
6. AWS S3 credentials for file storage
7. GitHub account with repository access

## Server Setup

### 1. Update System Packages

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Docker and Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 3. Create Deployment Directory

```bash
sudo mkdir -p /opt/virtualcoworking
sudo chown $USER:$USER /opt/virtualcoworking
cd /opt/virtualcoworking
```

### 4. Clone Repository

```bash
git clone https://github.com/yourusername/virtualcoworking.git .
```

## Configuration

### 1. Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your production values:

```bash
# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=virtualcoworking
DB_USER=vcuser
DB_PASSWORD=your_secure_password
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Email
EMAIL_HOST=smtp.yourprovider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# AWS S3
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Django
SECRET_KEY=your_very_secure_secret_key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost,127.0.0.1

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### 2. Nginx Configuration

Update the Nginx configuration in `infrastructure/nginx/nginx.conf`:

1. Replace `yourdomain.com` with your actual domain
2. Update SSL certificate paths after obtaining certificates

### 3. Certbot Configuration

Update the Certbot command in `docker-compose.yml`:

```yaml
command: certonly --webroot --webroot-path=/var/www/certbot --email your@email.com --agree-tos --no-eff-email -d yourdomain.com -d www.yourdomain.com
```

## Deployment Process

### 1. Initial Setup

```bash
# Navigate to infrastructure directory
cd infrastructure

# Create necessary directories
mkdir -p nginx/certbot/conf nginx/certbot/www

# Start services
docker-compose up -d
```

### 2. Obtain SSL Certificates

```bash
# Run Certbot to obtain certificates
docker-compose run --rm certbot

# Update Nginx configuration with actual certificate paths
# Edit nginx/nginx.conf to point to:
# ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
# ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

# Restart Nginx
docker-compose restart nginx
```

### 3. Database Setup

```bash
# Run database migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Collect static files
docker-compose exec backend python manage.py collectstatic --noinput
```

### 4. Start Celery Workers

```bash
# The Celery workers should already be running via docker-compose
# Check their status
docker-compose ps
```

## Monitoring and Maintenance

### 1. View Logs

```bash
# View backend logs
docker-compose logs -f backend

# View frontend logs
docker-compose logs -f frontend

# View database logs
docker-compose logs -f db

# View all logs
docker-compose logs -f
```

### 2. Backup Database

```bash
# Create database backup
docker-compose exec db pg_dump -U postgres virtualcoworking > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database (if needed)
# docker-compose exec -T db psql -U postgres virtualcoworking < backup_file.sql
```

### 3. Update Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart services
cd infrastructure
docker-compose down
docker-compose up --build -d

# Run migrations if needed
docker-compose exec backend python manage.py migrate
```

### 4. Renew SSL Certificates

```bash
# Certbot certificates are automatically renewed by the Certbot container
# Check renewal status
docker-compose exec certbot certbot certificates
```

## Scaling Considerations

### Horizontal Scaling

1. **Backend**: Scale Django application containers:
   ```bash
   docker-compose up --scale backend=3 -d
   ```

2. **Frontend**: Scale Next.js application containers:
   ```bash
   docker-compose up --scale frontend=3 -d
   ```

3. **Database**: For high-traffic applications, consider:
   - Database read replicas
   - Connection pooling
   - Query optimization

### Performance Tuning

1. **Django**:
   - Enable database connection pooling
   - Use Redis for caching
   - Optimize database queries
   - Enable GZip compression

2. **PostgreSQL**:
   - Tune memory settings (shared_buffers, work_mem)
   - Enable query planner statistics
   - Regularly vacuum and analyze tables

3. **Nginx**:
   - Enable HTTP/2
   - Configure caching headers
   - Optimize worker processes

## Security Best Practices

1. **Firewall**:
   ```bash
   sudo ufw enable
   sudo ufw allow ssh
   sudo ufw allow 80
   sudo ufw allow 443
   ```

2. **Regular Updates**:
   ```bash
   # Update system packages
   sudo apt update && sudo apt upgrade -y
   
   # Update Docker images
   docker-compose pull
   docker-compose up -d
   ```

3. **Monitoring**:
   - Set up log aggregation (ELK stack or similar)
   - Implement application performance monitoring (APM)
   - Set up uptime monitoring

## Troubleshooting

### Common Issues

1. **Permission Denied Errors**:
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER /opt/virtualcoworking
   ```

2. **Database Connection Issues**:
   ```bash
   # Check database status
   docker-compose exec db pg_isready
   
   # Check database logs
   docker-compose logs db
   ```

3. **SSL Certificate Issues**:
   ```bash
   # Check certificate status
   docker-compose exec certbot certbot certificates
   
   # Renew certificates manually
   docker-compose run --rm certbot certbot renew
   ```

4. **Application Not Starting**:
   ```bash
   # Check container status
   docker-compose ps
   
   # Check specific container logs
   docker-compose logs backend
   ```

### Emergency Procedures

1. **Rollback to Previous Version**:
   ```bash
   # If using git tags
   git checkout v1.0.0
   docker-compose down
   docker-compose up --build -d
   ```

2. **Restore Database from Backup**:
   ```bash
   # Stop application
   docker-compose down
   
   # Restore database
   docker-compose up -d db
   sleep 10
   docker-compose exec -T db psql -U postgres virtualcoworking < backup_file.sql
   
   # Start application
   docker-compose up -d
   ```

## Support and Maintenance Schedule

### Daily
- Check application logs
- Monitor disk space usage
- Verify SSL certificate validity

### Weekly
- Update system packages
- Review security logs
- Test backup restoration process

### Monthly
- Review and optimize database performance
- Update dependencies
- Conduct security audit

### Quarterly
- Review and update security policies
- Conduct penetration testing
- Update disaster recovery plan