# Deployment Guide

Complete guide for deploying the AI Interview Assistant to production.

## Architecture Overview

```
Frontend (Vercel) → Backend (Railway) → Database (MongoDB Atlas)
```

## Prerequisites

- GitHub account
- Vercel account
- Railway or Render account
- MongoDB Atlas account

## Step 1: Setup MongoDB Atlas (Database)

### Create Database

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up or log in
3. Create a new project: "AI Interview Assistant"
4. Click "Build a Database"
5. Choose **M0 FREE** tier
6. Select your cloud provider and region
7. Create cluster (takes 3-5 minutes)

### Configure Access

1. **Database Access**
   - Click "Database Access" in left sidebar
   - Click "Add New Database User"
   - Choose "Password" authentication
   - Username: `interview_admin`
   - Generate secure password (save it!)
   - Database User Privileges: "Read and write to any database"
   - Add User

2. **Network Access**
   - Click "Network Access" in left sidebar
   - Click "Add IP Address"
   - Choose "Allow Access from Anywhere" (0.0.0.0/0)
   - For production: Add specific IPs only
   - Confirm

### Get Connection String

1. Click "Database" in left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Driver: Python, Version: 3.12 or later
5. Copy connection string:
   ```
   mongodb+srv://interview_admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace `<password>` with your actual password
7. Save this for later

### Initialize Database

1. Update `scripts/setup_mongodb.py` with your connection string
2. Run the setup script:
   ```bash
   cd scripts
   python setup_mongodb.py
   ```
3. Verify collections created in Atlas dashboard

## Step 2: Deploy Backend (Railway)

### Create Railway Project

1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Choose "Deploy from GitHub repo"
5. Select your repository
6. Choose "backend" as root directory (if needed)

### Configure Backend Service

1. **Environment Variables**
   - Click on your service
   - Go to "Variables" tab
   - Add these variables:
     ```
     MONGODB_URL=mongodb+srv://interview_admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/ai_interview_assistant?retryWrites=true&w=majority
     API_HOST=0.0.0.0
     API_PORT=$PORT
     CORS_ORIGINS=https://your-frontend.vercel.app
     ```

2. **Build Configuration**
   - Railway auto-detects Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Root Directory: `/backend`

3. **Deploy**
   - Click "Deploy"
   - Wait for deployment (2-3 minutes)
   - Note your backend URL: `https://your-app.railway.app`

4. **Verify Deployment**
   - Visit: `https://your-app.railway.app`
   - Should see: `{"message":"AI Interview Assistant API","status":"online"}`
   - Check API docs: `https://your-app.railway.app/docs`

### Alternative: Deploy to Render

1. Go to [Render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your repository
5. Configure:
   - Name: `ai-interview-backend`
   - Root Directory: `backend`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables (same as Railway)
7. Create Web Service

## Step 3: Deploy Frontend (Vercel)

### Create Vercel Project

1. Go to [Vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "Add New..." → "Project"
4. Import your GitHub repository
5. Configure project:
   - Framework Preset: Next.js
   - Root Directory: `./` (project root)
   - Build Command: `npm run build`
   - Output Directory: `.next`

### Configure Environment Variables

1. In project settings, go to "Environment Variables"
2. Add variable:
   ```
   NEXT_PUBLIC_API_URL=https://your-app.railway.app
   ```
3. Apply to: Production, Preview, Development

### Deploy

1. Click "Deploy"
2. Wait for build (2-4 minutes)
3. Visit your site: `https://your-project.vercel.app`

### Custom Domain (Optional)

1. Go to "Settings" → "Domains"
2. Add your custom domain
3. Update DNS records as instructed
4. SSL certificate auto-generated

## Step 4: Update CORS

After deploying frontend, update backend CORS:

1. Go to Railway/Render backend settings
2. Update `CORS_ORIGINS` environment variable:
   ```
   CORS_ORIGINS=https://your-project.vercel.app,https://www.yourdomain.com
   ```
3. Redeploy backend

## Step 5: Testing

### Test Complete Flow

1. Visit your frontend URL
2. Click "Start Interview"
3. Complete setup wizard
4. Conduct interview
5. View results
6. Check backend logs for any errors

### Verify API Connectivity

```bash
# Test backend health
curl https://your-app.railway.app/

# Test interview creation
curl -X POST https://your-app.railway.app/api/interviews \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "Test User",
    "candidate_email": "test@example.com",
    "role": "Frontend Developer",
    "experience_level": "mid",
    "skills": ["React", "TypeScript"],
    "duration": 30
  }'
```

## Monitoring

### Railway Monitoring

- Click "Observability" tab
- View logs, metrics, and traces
- Set up alerts for errors

### Vercel Analytics

- Enable Vercel Analytics in project settings
- View real-time traffic and performance
- Monitor Core Web Vitals

### MongoDB Atlas Monitoring

- Dashboard shows database metrics
- Set up performance alerts
- Monitor query performance

## Production Checklist

- [ ] MongoDB Atlas cluster created and initialized
- [ ] Backend deployed with correct environment variables
- [ ] Frontend deployed and connecting to backend
- [ ] CORS configured correctly
- [ ] All API endpoints working
- [ ] Interview flow tested end-to-end
- [ ] Error logging configured
- [ ] Database backups enabled
- [ ] SSL certificates active
- [ ] Custom domain configured (optional)

## Troubleshooting

### Frontend can't reach backend

1. Check NEXT_PUBLIC_API_URL is correct
2. Verify backend is running
3. Check CORS settings
4. Look at browser network tab

### Database connection errors

1. Verify MONGODB_URL is correct
2. Check password doesn't have special characters (URL encode if needed)
3. Verify IP whitelist includes 0.0.0.0/0
4. Check database user permissions

### Backend crashes

1. Check Railway/Render logs
2. Verify all environment variables set
3. Check Python dependencies installed
4. Verify MongoDB connection string

### Slow performance

1. Check MongoDB Atlas region (should be close to backend)
2. Enable database indexes (setup script does this)
3. Monitor Railway/Render metrics
4. Consider upgrading to paid tiers

## Scaling

### Database Scaling

- Upgrade MongoDB Atlas tier for more storage/performance
- Enable sharding for large datasets
- Add read replicas for better read performance

### Backend Scaling

- Railway: Auto-scales with traffic
- Render: Choose higher instance sizes
- Consider load balancing for high traffic

### Frontend Scaling

- Vercel handles scaling automatically
- Enable Edge Network for global CDN
- Implement ISR for better performance

## Security Best Practices

1. **Environment Variables**
   - Never commit .env files
   - Use different credentials for dev/prod
   - Rotate secrets regularly

2. **Database**
   - Use strong passwords
   - Enable database encryption
   - Regular backups
   - Whitelist specific IPs in production

3. **API**
   - Implement rate limiting
   - Add authentication for sensitive operations
   - Validate all inputs
   - Use HTTPS only

4. **Frontend**
   - Enable CSP headers
   - Sanitize user inputs
   - Use environment variables for API URLs

## Cost Estimates

### Free Tier (Development)

- MongoDB Atlas: Free (M0 cluster, 512MB)
- Railway: $5/month credit (enough for small apps)
- Vercel: Free (hobby plan)
- **Total: $0-5/month**

### Production (Small Scale)

- MongoDB Atlas: $9/month (M2 cluster, 2GB)
- Railway: ~$10-20/month
- Vercel: Free (upgrade if needed)
- **Total: ~$20-30/month**

### Production (Medium Scale)

- MongoDB Atlas: $25-50/month (M10 cluster)
- Railway: $20-50/month
- Vercel Pro: $20/month
- **Total: ~$65-120/month**

## Support

For deployment issues:
- Railway: https://railway.app/help
- Vercel: https://vercel.com/support
- MongoDB Atlas: https://www.mongodb.com/cloud/atlas/support

---

**Deployment Complete!** Your AI Interview Assistant is now live. 🚀
