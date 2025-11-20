# Deployment Guide

## Backend Deployment (Django)

### Option 1: Render (Recommended for MVP)

1. Create a Render account at https://render.com/

2. Create a new Web Service:
   - Connect your GitHub repository
   - Set Build Command: `pip install -r requirements.txt`
   - Set Start Command: `gunicorn virtualcoworking.wsgi:application`
   - Set Python version to 3.12 or higher
   - Add environment variables:
     - `SECRET_KEY` - Django secret key
     - `DEBUG` - Set to False for production
     - `DATABASE_URL` - PostgreSQL database URL (Render provides this automatically)
     - `ALLOWED_HOSTS` - Your Render app URL

3. Create a PostgreSQL database on Render:
   - Link it to your web service
   - Render will automatically set the DATABASE_URL environment variable

4. Deploy the service

### Option 2: Heroku

1. Create a Heroku account at https://heroku.com/

2. Install Heroku CLI:
   ```bash
   brew tap heroku/brew && brew install heroku
   ```

3. Login to Heroku:
   ```bash
   heroku login
   ```

4. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

5. Add PostgreSQL addon:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

6. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   ```

7. Add Procfile:
   ```
   web: gunicorn virtualcoworking.wsgi:application
   ```

8. Deploy:
   ```bash
   git push heroku main
   ```

9. Run migrations:
   ```bash
   heroku run python manage.py migrate
   ```

### Option 3: Self-hosted (VPS)

1. Set up a Linux server (Ubuntu/Debian recommended)

2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib
   ```

3. Create database and user:
   ```sql
   sudo -u postgres psql
   CREATE DATABASE virtualcoworking;
   CREATE USER vcuser WITH PASSWORD 'your-password';
   ALTER ROLE vcuser SET client_encoding TO 'utf8';
   ALTER ROLE vcuser SET default_transaction_isolation TO 'read committed';
   ALTER ROLE vcuser SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE virtualcoworking TO vcuser;
   \q
   ```

4. Clone repository and set up virtual environment:
   ```bash
   git clone your-repo-url
   cd virtualcoworking/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. Configure environment variables in a `.env` file:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   DATABASE_URL=postgresql://vcuser:your-password@localhost/virtualcoworking
   ALLOWED_HOSTS=your-domain.com
   ```

6. Run migrations:
   ```bash
   python manage.py migrate
   ```

7. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

9. Set up Gunicorn:
   ```bash
   pip install gunicorn
   ```

10. Create systemd service file (`/etc/systemd/system/virtualcoworking.service`):
    ```
    [Unit]
    Description=Virtual Coworking Gunicorn daemon
    After=network.target

    [Service]
    User=your-user
    Group=www-data
    WorkingDirectory=/path/to/virtualcoworking/backend
    ExecStart=/path/to/virtualcoworking/backend/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/path/to/virtualcoworking/virtualcoworking.sock virtualcoworking.wsgi:application

    [Install]
    WantedBy=multi-user.target
    ```

11. Start and enable the service:
    ```bash
    sudo systemctl start virtualcoworking
    sudo systemctl enable virtualcoworking
    ```

12. Configure Nginx:
    Create `/etc/nginx/sites-available/virtualcoworking`:
    ```
    server {
        listen 80;
        server_name your-domain.com;

        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /path/to/virtualcoworking/backend;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/path/to/virtualcoworking/backend/virtualcoworking.sock;
        }
    }
    ```

13. Enable the site:
    ```bash
    sudo ln -s /etc/nginx/sites-available/virtualcoworking /etc/nginx/sites-enabled
    sudo nginx -t
    sudo systemctl restart nginx
    ```

## Frontend Deployment (Next.js)

### Option 1: Vercel (Recommended)

1. Create a Vercel account at https://vercel.com/

2. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

3. Navigate to frontend directory:
   ```bash
   cd frontend/virtual-coworking
   ```

4. Deploy:
   ```bash
   vercel
   ```

5. Follow the prompts to connect to your GitHub repository

6. Set environment variables in Vercel dashboard:
   - `NEXT_PUBLIC_API_URL` - Your backend API URL

### Option 2: Self-hosted

1. Build the application:
   ```bash
   npm run build
   ```

2. Start the production server:
   ```bash
   npm start
   ```

3. For production, use a process manager like PM2:
   ```bash
   npm install -g pm2
   pm2 start npm --name "virtual-coworking" -- start
   ```

4. Set up reverse proxy with Nginx:
   ```
   server {
       listen 80;
       server_name frontend.your-domain.com;

       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

## Environment Variables

### Backend (.env)
```
SECRET_KEY=your-django-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=your-domain.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://frontend.your-domain.com,http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://api.your-domain.com
```

## SSL Certificate

For production deployment, you should use HTTPS. You can obtain a free SSL certificate from Let's Encrypt:

1. Install Certbot:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. Obtain certificate:
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

3. Follow the prompts to configure automatic renewal

## Monitoring and Logging

### Backend
- Use Django's built-in logging
- Consider using Sentry for error tracking
- Set up log rotation with logrotate

### Frontend
- Use Vercel's built-in analytics
- Consider using Sentry for frontend error tracking

## Backup Strategy

### Database Backup
1. For Render/Heroku: Use built-in backup features
2. For self-hosted: Set up automated PostgreSQL backups
   ```bash
   pg_dump virtualcoworking > backup.sql
   ```

### File Backup
- For uploaded files, consider using cloud storage (AWS S3, Google Cloud Storage)
- Set up regular sync to backup storage

## Scaling Considerations

### Horizontal Scaling
- Use Redis for Django Channels layer
- Use a CDN for static files
- Consider database read replicas for analytics queries

### Vertical Scaling
- Monitor resource usage
- Upgrade server resources as needed
- Optimize database queries with indexing

## Maintenance

### Regular Tasks
- Update dependencies regularly
- Monitor application logs
- Review and rotate API keys
- Update SSL certificates
- Perform database maintenance (VACUUM, ANALYZE)

### Security
- Keep all dependencies updated
- Regularly review access controls
- Implement rate limiting
- Use security headers in Nginx
- Regularly audit user permissions