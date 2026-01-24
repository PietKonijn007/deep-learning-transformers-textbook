# Deployment Guide

## Local Development

### Quick Start
```bash
cd nodejs-version
npm install
npm run dev
```

Access at: `http://localhost:3000`

## Production Deployment

### Option 1: Traditional Node.js Hosting

#### Requirements
- Node.js 14.0.0 or higher
- npm
- 256MB RAM minimum
- 50MB disk space

#### Steps
```bash
# 1. Upload files to server
scp -r nodejs-version user@server:/path/to/app

# 2. SSH into server
ssh user@server

# 3. Navigate to app directory
cd /path/to/app/nodejs-version

# 4. Install dependencies (production only)
npm install --production

# 5. Start the server
npm start
```

#### Using PM2 (Recommended)
```bash
# Install PM2 globally
npm install -g pm2

# Start app with PM2
pm2 start server.js --name "dl-textbook"

# Save PM2 configuration
pm2 save

# Setup auto-restart on reboot
pm2 startup
```

### Option 2: Heroku

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Steps
```bash
# 1. Login to Heroku
heroku login

# 2. Create new app
heroku create your-app-name

# 3. Deploy
git subtree push --prefix nodejs-version heroku main

# 4. Open app
heroku open
```

#### Heroku Configuration
Create `Procfile` in nodejs-version:
```
web: node server.js
```

### Option 3: Vercel

#### Prerequisites
- Vercel account
- Vercel CLI installed

#### Steps
```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Navigate to nodejs-version
cd nodejs-version

# 3. Deploy
vercel

# 4. Follow prompts
```

#### Vercel Configuration
Create `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "server.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "server.js"
    }
  ]
}
```

### Option 4: Docker

#### Dockerfile
Create `Dockerfile` in nodejs-version:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```

#### Build and Run
```bash
# Build image
docker build -t dl-textbook .

# Run container
docker run -p 3000:3000 dl-textbook

# Or with docker-compose
docker-compose up
```

#### docker-compose.yml
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    restart: unless-stopped
    environment:
      - NODE_ENV=production
```

### Option 5: DigitalOcean App Platform

#### Steps
1. Push code to GitHub
2. Go to DigitalOcean App Platform
3. Create new app from GitHub repo
4. Select `nodejs-version` directory
5. Configure:
   - Build Command: `npm install`
   - Run Command: `npm start`
   - Port: 3000
6. Deploy

### Option 6: AWS EC2

#### Steps
```bash
# 1. SSH into EC2 instance
ssh -i key.pem ec2-user@your-instance

# 2. Install Node.js
curl -sL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo yum install -y nodejs

# 3. Clone or upload code
git clone your-repo
cd your-repo/nodejs-version

# 4. Install dependencies
npm install --production

# 5. Install PM2
sudo npm install -g pm2

# 6. Start app
pm2 start server.js

# 7. Configure nginx (optional)
sudo yum install nginx
```

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

## Environment Configuration

### Environment Variables

```bash
# Port (default: 3000)
PORT=8080

# Node environment
NODE_ENV=production
```

### Setting Environment Variables

#### Linux/Mac
```bash
export PORT=8080
export NODE_ENV=production
npm start
```

#### Windows
```cmd
set PORT=8080
set NODE_ENV=production
npm start
```

#### .env file (with dotenv)
```bash
# Install dotenv
npm install dotenv

# Create .env file
PORT=8080
NODE_ENV=production
```

## Performance Optimization

### Enable Compression
Already enabled in `server.js` via compression middleware.

### Enable Caching
Static files cached for 1 day by default.

### Use CDN
For production, consider using a CDN for static assets:
```javascript
// In server.js
app.use('/static', express.static('public', {
  maxAge: '7d'
}));
```

### Enable HTTPS
Use Let's Encrypt for free SSL:
```bash
sudo certbot --nginx -d your-domain.com
```

## Monitoring

### PM2 Monitoring
```bash
# View logs
pm2 logs

# Monitor resources
pm2 monit

# View status
pm2 status
```

### Health Check Endpoint
Add to `server.js`:
```javascript
app.get('/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});
```

## Backup & Recovery

### Backup Strategy
1. Code: Use Git
2. Dependencies: package.json and package-lock.json
3. Configuration: Environment variables documented

### Recovery
```bash
# Clone repo
git clone your-repo

# Install dependencies
npm install

# Configure environment
export PORT=3000

# Start
npm start
```

## Scaling

### Horizontal Scaling
Use PM2 cluster mode:
```bash
pm2 start server.js -i max
```

### Load Balancing
Use nginx or cloud load balancer to distribute traffic.

### Database (if needed)
Currently stateless - no database required.

## Security Checklist

- [ ] Use HTTPS in production
- [ ] Set NODE_ENV=production
- [ ] Keep dependencies updated
- [ ] Use environment variables for config
- [ ] Enable rate limiting (if needed)
- [ ] Set proper CORS headers
- [ ] Use helmet.js for security headers
- [ ] Regular security audits: `npm audit`

## Troubleshooting

### App won't start
```bash
# Check Node version
node --version

# Check port availability
lsof -i :3000

# Check logs
pm2 logs
```

### Chapters not loading
- Verify `../docs/chapters/` directory exists
- Check file permissions
- Review server logs

### High memory usage
- Restart app: `pm2 restart all`
- Check for memory leaks
- Monitor with: `pm2 monit`

## Cost Estimates

### Hosting Options
- **Heroku**: Free tier available, $7/month for hobby
- **Vercel**: Free tier available
- **DigitalOcean**: $5/month droplet
- **AWS EC2**: $3-10/month (t2.micro)
- **VPS**: $5-20/month

### Bandwidth
- Average page: ~100KB compressed
- 10,000 views/month: ~1GB bandwidth
- Most hosts include sufficient bandwidth

## Maintenance

### Regular Tasks
```bash
# Update dependencies
npm update

# Security audit
npm audit fix

# Restart app
pm2 restart all

# View logs
pm2 logs --lines 100
```

### Monitoring Checklist
- [ ] Server uptime
- [ ] Response times
- [ ] Error rates
- [ ] Memory usage
- [ ] Disk space
- [ ] SSL certificate expiry

## Support

For deployment issues:
1. Check logs: `pm2 logs` or `heroku logs`
2. Verify environment variables
3. Test locally first
4. Check firewall/security groups
5. Review hosting provider docs
