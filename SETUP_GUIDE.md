# 🚀 AuraStyle - Setup & Deployment Guide

**Production-Ready E-Commerce Recommendation System**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (Local Development)](#quick-start-local-development)
3. [Docker Setup](#docker-setup)
4. [Manual Setup](#manual-setup)
5. [Production Deployment](#production-deployment)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software:
- **Python 3.11+** ([Download](https://www.python.org/downloads/))
- **Node.js 20+** ([Download](https://nodejs.org/))
- **Git** ([Download](https://git-scm.com/))

### Optional (Recommended):
- **Docker & Docker Compose** ([Download](https://www.docker.com/))
- **PostgreSQL 15+** (for production)
- **Redis 7+** (for caching)

### System Requirements:
- **RAM:** 4GB minimum, 8GB recommended
- **Disk:** 2GB free space
- **OS:** Windows 10/11, macOS, or Linux

---

## Quick Start (Local Development)

### Option 1: One-Command Startup (Windows)

```bash
# Clone the repository (if not already)
git clone <your-repo-url>
cd Microproject

# Run the startup script
.\run_pro.bat
```

This will:
1. Start the backend on `http://localhost:8000`
2. Start the frontend on `http://localhost:3000`
3. Open your browser automatically

### Option 2: Docker Compose (Recommended)

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your settings (optional for local dev)

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

**Services Started:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

---

## Docker Setup

### Building Images

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend
```

### Managing Services

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart a service
docker-compose restart backend

# View logs
docker-compose logs -f backend

# Execute commands in container
docker-compose exec backend python seed.py
docker-compose exec backend pytest
```

### Database Operations

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Seed database
docker-compose exec backend python seed.py

# Access PostgreSQL
docker-compose exec db psql -U aurastyle_user -d aurastyle

# Backup database
docker-compose exec db pg_dump -U aurastyle_user aurastyle > backup.sql

# Restore database
docker-compose exec -T db psql -U aurastyle_user aurastyle < backup.sql
```

---

## Manual Setup

### Backend Setup

```bash
# Navigate to server directory
cd server

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp ../.env.example .env

# Edit .env with your settings

# Seed database with sample data
python seed.py

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:** http://localhost:8000

### Frontend Setup

```bash
# Navigate to frontend directory
cd client-pro

# Install dependencies
npm install

# Copy environment file (if needed)
# Create .env.local with:
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Start development server
npm run dev
```

**Frontend will be available at:** http://localhost:3000

---

## Production Deployment

### Option 1: Vercel (Frontend) + Render (Backend)

#### Deploy Frontend to Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   cd client-pro
   vercel
   ```

3. **Set Environment Variables:**
   - Go to Vercel Dashboard → Project Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_URL=https://your-backend-url.com`

4. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

#### Deploy Backend to Render

1. **Create `render.yaml`:**
   ```yaml
   services:
     - type: web
       name: aurastyle-backend
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
       envVars:
         - key: DATABASE_URL
           fromDatabase:
             name: aurastyle-db
             property: connectionString
         - key: REDIS_URL
           fromService:
             name: aurastyle-redis
             type: redis
             property: connectionString
         - key: SECRET_KEY
           generateValue: true
         - key: ENVIRONMENT
           value: production
         - key: DEBUG
           value: false
   
   databases:
     - name: aurastyle-db
       databaseName: aurastyle
       user: aurastyle_user
   ```

2. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add Render configuration"
   git push
   ```

3. **Deploy on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - New → Blueprint
   - Connect your GitHub repository
   - Render will auto-deploy

### Option 2: Railway (Full Stack)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Add PostgreSQL
railway add --database postgres

# Add Redis
railway add --database redis

# Deploy
railway up
```

### Option 3: AWS/GCP/Azure

#### Using Docker Images:

```bash
# Build production images
docker build -t aurastyle-backend:latest ./server
docker build -t aurastyle-frontend:latest ./client-pro

# Tag for registry
docker tag aurastyle-backend:latest your-registry/aurastyle-backend:latest
docker tag aurastyle-frontend:latest your-registry/aurastyle-frontend:latest

# Push to registry
docker push your-registry/aurastyle-backend:latest
docker push your-registry/aurastyle-frontend:latest

# Deploy to Kubernetes/ECS/Cloud Run
```

---

## Testing

### Backend Tests

```bash
cd server

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_recommender.py

# Run with verbose output
pytest -v
```

### Frontend Tests

```bash
cd client-pro

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run E2E tests (if configured)
npm run test:e2e
```

### API Testing

```bash
# Health check
curl http://localhost:8000/health

# Get products
curl http://localhost:8000/api/products

# Get recommendations
curl http://localhost:8000/api/recommendations/trending

# Test authentication
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

---

## Configuration

### Environment Variables

**Backend (.env):**
```env
# Required
SECRET_KEY=your_secret_key_min_32_characters
DATABASE_URL=postgresql://user:pass@localhost:5432/aurastyle

# Optional
REDIS_URL=redis://localhost:6379/0
ENVIRONMENT=production
DEBUG=false
RATE_LIMIT_PER_MINUTE=60
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Database Migration

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Monitoring & Maintenance

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "checks": {
    "database": "healthy",
    "cache": "healthy",
    "ml_engine": "loaded"
  }
}
```

### Logs

```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Application logs (if running manually)
tail -f server/logs/app.log
```

### Performance Monitoring

```bash
# View metrics
curl http://localhost:8000/metrics

# Response time
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/products
```

**curl-format.txt:**
```
time_total: %{time_total}s
```

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

#### 2. Database Connection Error

```bash
# Check PostgreSQL is running
docker-compose ps db

# Restart database
docker-compose restart db

# Check connection string
echo $DATABASE_URL
```

#### 3. Redis Connection Error

```bash
# Check Redis is running
docker-compose ps redis

# Test connection
redis-cli ping

# Restart Redis
docker-compose restart redis
```

#### 4. Module Not Found

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or for frontend
npm install --force
```

#### 5. CORS Errors

- Check `CORS_ORIGINS` in backend config
- Ensure frontend URL is whitelisted
- In development, CORS is set to allow all origins

#### 6. Slow Recommendations

```bash
# Check if Redis is running
curl http://localhost:8000/health

# Retrain model
curl -X POST http://localhost:8000/api/recommendations/retrain

# Clear cache
redis-cli FLUSHALL
```

---

## Performance Optimization

### Backend

1. **Enable Redis Caching:**
   ```env
   REDIS_URL=redis://localhost:6379/0
   ```

2. **Increase Workers:**
   ```bash
   uvicorn app.main:app --workers 4
   ```

3. **Use PostgreSQL:**
   ```env
   DATABASE_URL=postgresql://user:pass@localhost:5432/aurastyle
   ```

### Frontend

1. **Build for Production:**
   ```bash
   npm run build
   npm start
   ```

2. **Enable Image Optimization:**
   - Use Next.js Image component
   - Configure image domains in `next.config.js`

3. **Enable Caching:**
   - Configure CDN (Vercel, Cloudflare)
   - Set appropriate cache headers

---

## Security Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Use HTTPS in production
- [ ] Set `DEBUG=false` in production
- [ ] Configure `CORS_ORIGINS` whitelist
- [ ] Use strong database passwords
- [ ] Enable rate limiting
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets
- [ ] Enable security headers
- [ ] Regular security audits

---

## Backup & Recovery

### Database Backup

```bash
# Automated daily backup (cron job)
0 2 * * * docker-compose exec db pg_dump -U aurastyle_user aurastyle > /backups/db_$(date +\%Y\%m\%d).sql
```

### Restore from Backup

```bash
docker-compose exec -T db psql -U aurastyle_user aurastyle < backup.sql
```

---

## Support

### Documentation
- API Docs: http://localhost:8000/docs
- Technical Docs: `TECHNICAL_DOCS.md`
- Roadmap: `PRODUCTION_ROADMAP.md`

### Logs
- Backend: `server/logs/`
- Frontend: Browser console

### Getting Help
1. Check this guide
2. Review error logs
3. Check GitHub issues
4. Contact support

---

## Next Steps

1. ✅ Complete setup
2. ✅ Verify all services running
3. ✅ Test API endpoints
4. ✅ Seed database
5. ✅ Test recommendations
6. 🔄 Deploy to staging
7. 🔄 Run load tests
8. 🔄 Deploy to production

---

**Happy Deploying! 🚀**
