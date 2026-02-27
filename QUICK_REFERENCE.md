# ⚡ Quick Reference Card - AuraStyle Platform

**One-page guide for common tasks**

---

## 🚀 Quick Start

### Start Everything (Docker)
```bash
docker-compose up -d
```

### Start Backend Only
```bash
cd server
venv\Scripts\activate
uvicorn app.main:app --reload
```

### Start Frontend Only
```bash
cd client-pro
npm run dev
```

---

## 🔗 Important URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |
| Metrics | http://localhost:8000/metrics |

---

## 🧪 Testing Commands

```bash
# Health check
curl http://localhost:8000/health

# Get products
curl http://localhost:8000/api/products

# Get trending
curl http://localhost:8000/api/recommendations/trending

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

---

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend

# Restart service
docker-compose restart backend

# Rebuild images
docker-compose build

# Seed database
docker-compose exec backend python seed.py
```

---

## 📊 Key Files

### Configuration
- `.env` - Environment variables
- `server/app/core/config.py` - App settings
- `docker-compose.yml` - Container orchestration

### Core Backend
- `server/app/main.py` - FastAPI application
- `server/app/ml/engine_v2.py` - ML recommendation engine
- `server/app/core/middleware.py` - Request processing
- `server/app/core/exceptions.py` - Error handling
- `server/app/core/cache.py` - Redis caching

### Frontend
- `client-pro/app/page.tsx` - Homepage
- `client-pro/components/Navbar.tsx` - Navigation
- `client-pro/lib/api.ts` - API client

---

## 🔧 Common Tasks

### Seed Database
```bash
cd server
python seed.py
```

### Clear Cache
```bash
redis-cli FLUSHALL
```

### View Logs
```bash
# Docker
docker-compose logs -f

# Manual
tail -f server/logs/app.log
```

### Retrain ML Model
```bash
curl -X POST http://localhost:8000/api/recommendations/retrain
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Database Connection Error
```bash
docker-compose restart db
```

### Redis Connection Error
```bash
docker-compose restart redis
```

### Module Not Found
```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Documentation

- **Setup Guide**: `SETUP_GUIDE.md`
- **Roadmap**: `PRODUCTION_ROADMAP.md`
- **Progress**: `PROGRESS_REPORT.md`
- **Summary**: `TRANSFORMATION_SUMMARY.md`
- **Technical**: `TECHNICAL_DOCS.md`

---

## 🎯 Next Steps Checklist

- [ ] Test local deployment
- [ ] Review documentation
- [ ] Customize configuration
- [ ] Add real product data
- [ ] Deploy to staging
- [ ] Write tests
- [ ] Production launch

---

**Quick Help:** See `SETUP_GUIDE.md` for detailed instructions
