# Deployment Guide

## Overview

This guide covers different deployment options for the AMR Detection System.

---

## Local Development

### Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/amr-detection.git
cd amr-detection

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python run_app.py
```

The app will be available at `http://localhost:8501`

---

## Docker Deployment

### Prerequisites
- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose (optional)

### Using Docker Compose (Recommended)

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f amr-detection

# Stop application
docker-compose down
```

### Using Docker Directly

```bash
# Build image
docker build -t amr-detection:latest .

# Run container
docker run -p 8501:8501 \
  -v $(pwd)/Models:/app/Models \
  -v $(pwd)/Dataset:/app/Dataset \
  -v $(pwd)/results:/app/results \
  amr-detection:latest

# For GPU support
docker run --gpus all -p 8501:8501 \
  -v $(pwd)/Models:/app/Models \
  amr-detection:latest
```

---

## Cloud Deployment

### AWS Deployment

#### Option 1: AWS ECS (Recommended)

```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name amr-detection

# 2. Push Docker image
docker build -t amr-detection:latest .
docker tag amr-detection:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/amr-detection:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/amr-detection:latest

# 3. Create ECS task definition (See AWS documentation)
# 4. Create ECS service
```

#### Option 2: AWS Lightsail

1. Sign into AWS Lightsail
2. Create new container service
3. Upload the Docker image
4. Deploy and configure public endpoint

### Heroku Deployment

```bash
# 1. Install Heroku CLI
# 2. Login to Heroku
heroku login

# 3. Create app
heroku create your-app-name

# 4. Set buildpack
heroku buildpacks:set heroku/docker

# 5. Deploy
git push heroku main

# 6. View logs
heroku logs --tail
```

**Note:** Heroku's free tier has Limited resources. Consider paid options for production.

### Google Cloud Run

```bash
# 1. Build and push image
gcloud builds submit --tag gcr.io/PROJECT-ID/amr-detection

# 2. Deploy
gcloud run deploy amr-detection \
  --image gcr.io/PROJECT-ID/amr-detection \
  --platform managed \
  --region us-central1 \
  --port 8501 \
  --memory 2Gi

# 3. Get URL
gcloud run services describe amr-detection
```

---

## Linux Server Deployment

### Using Systemd

Create `/etc/systemd/system/amr-detection.service`:

```ini
[Unit]
Description=AMR Detection System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/amr-detection
ExecStart=/opt/amr-detection/venv/bin/python run_app.py
Restart=always
Environment="PATH=/opt/amr-detection/venv/bin"

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl enable amr-detection
sudo systemctl start amr-detection
sudo systemctl status amr-detection
```

### Using Nginx (Reverse Proxy)

Create `/etc/nginx/sites-available/amr-detection`:

```nginx
upstream amr_app {
    server 127.0.0.1:8501;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://amr_app;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable and test:

```bash
sudo ln -s /etc/nginx/sites-available/amr-detection /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Performance Optimization

### For CPU-only systems:
- Use smaller model (`yolov8n` instead of `yolov8m`)
- Reduce input image size
- Lower detection frequency

### For GPU systems:
- Set `USE_GPU=true` in `.env`
- Use larger models for better accuracy
- Increase batch size

### Memory optimization:
- Docker: Set memory limits
- Application: Reduce MAX_LOG_ENTRIES

---

## Monitoring & Logging

### Application Logs
```bash
# Docker
docker logs -f amr-detection

# Systemd
journalctl -u amr-detection -f

# File-based
tail -f /var/log/amr-detection.log
```

### Health Checks
```bash
# Check if application is running
curl http://localhost:8501

# Docker health
docker inspect amr-detection
```

---

## Security Considerations

1. **Use HTTPS**: Deploy behind SSL/TLS proxy
2. **Authentication**: Add authentication layer (Nginx, reverse proxy)
3. **Environment Variables**: Never commit `.env` files
4. **Model Security**: Validate uploaded files
5. **Rate Limiting**: Implement rate limiting for API endpoints
6. **Updates**: Keep dependencies updated

### Example Nginx with Basic Auth
```nginx
server {
    listen 80;
    server_name your-domain.com;

    auth_basic "AMR Detection";
    auth_basic_user_file /etc/nginx/.htpasswd;

    location / {
        proxy_pass http://127.0.0.1:8501;
    }
}
```

---

## Troubleshooting

### Common Issues

**Model not found**
```bash
# Solution: Download and place model
mkdir -p Models
# Place best.pt in Models directory
```

**Permission denied (Docker)**
```bash
# Solution: Add user to docker group
sudo usermod -aG docker $USER
```

**Port already in use**
```bash
# Solution: Use different port
docker run -p 8502:8501 amr-detection:latest

# Or kill process using port
lsof -i :8501
kill -9 <PID>
```

**GPU not recognized**
```bash
# Solution: Install NVIDIA Docker
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
```

---

## Backup & Recovery

### Backup Strategy
```bash
# Backup models and results
tar -czf amr-detection-backup.tar.gz Models/ results/ Dataset/

# Upload to S3
aws s3 cp amr-detection-backup.tar.gz s3://your-bucket/
```

### Recovery
```bash
# Download backup
aws s3 cp s3://your-bucket/amr-detection-backup.tar.gz .

# Extract
tar -xzf amr-detection-backup.tar.gz
```

---

## Support

For deployment issues:
- Check logs: `docker logs` or `journalctl`
- Review [GitHub Issues](https://github.com/yourusername/amr-detection/issues)
- Create detailed issue with logs

---

**Last Updated:** 2024
