# 🧭 Leave Tracker - Team Absence Management

A **production-ready web application** built with **FastAPI (Python)** backend and **React (TypeScript)** frontend.  
Features secure **JWT authentication with 2FA**, comprehensive leave management, and **one-command deployment to Google Cloud (Free Tier)**.

---

## 🎯 Quick Start

### 🏃 Local Development
```powershell
# Press F5 in VS Code (both backend + frontend launch)
# Or manually:
cd backend; uvicorn app.main:app --reload
cd frontend; npm run dev
```

### ☁️ Deploy to Google Cloud (FREE)
```powershell
# One command deployment!
.\deploy-to-gcp.ps1 `
    -ProjectId "your-project-id" `
    -SecretKey "$(python -c 'import secrets; print(secrets.token_hex(32))')" `
    -DbPassword "your-secure-password"
```
**See**: [QUICK_DEPLOY_GCP.md](./QUICK_DEPLOY_GCP.md) | [Full Guide](./GOOGLE_CLOUD_DEPLOYMENT.md)

---

## ✨ Features

### Core Functionality
- 🔐 **Secure Authentication**: JWT tokens with 30-minute expiration
- 🔑 **2FA**: Google Authenticator integration with QR codes
- 👥 **People Management**: Add, edit, delete team members
- � **Leave Types**: Customizable leave categories
- 📅 **Absence Logging**: Track leaves with date, duration, type, reason
- ⚙️ **Settings Interface**: Tabbed UI for managing people and types
- 🎨 **Modern UI**: Material-UI components with responsive design

### Technical Features
- 🔒 **Custom Password Encryption**: Username encrypted with password-derived key
- 🛡️ **JWT Protection**: All API endpoints secured
- 🔄 **Automatic Token Handling**: Axios interceptors for seamless auth
- 📁 **Path Aliases**: Clean imports (`@services/api`)
- 🌐 **Environment Config**: Separate dev/prod configurations
- � **Docker Ready**: Containerized backend for easy deployment
- ☁️ **Cloud Native**: Optimized for Google Cloud Run + Cloud SQL

---

## 🏗️ Architecture

### Tech Stack
```
┌─────────────────────────────────────┐
│  Frontend (React 19 + TypeScript)   │
│  - Material-UI 7                    │
│  - React Router 7                   │
│  - Axios with JWT interceptors      │
│  - Path aliases (@services/*)       │
└──────────────┬──────────────────────┘
               │ REST API (JWT Bearer)
┌──────────────▼──────────────────────┐
│  Backend (FastAPI + Python 3.11)    │
│  - SQLAlchemy ORM                   │
│  - JWT Authentication               │
│  - Custom Password Encryption       │
│  - 2FA (TOTP/Google Authenticator)  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Database                            │
│  - SQLite (local dev)               │
│  - PostgreSQL (production/GCP)      │
└─────────────────────────────────────┘
```

### Google Cloud Deployment
```
┌─────────────────────────────────────┐
│  Cloud Storage + CDN (Frontend)     │
│  ✓ 5GB storage free                 │
│  ✓ 1GB egress free                  │
└─────────────────────────────────────┘
               │ HTTPS
┌──────────────▼──────────────────────┐
│  Cloud Run (Backend API)            │
│  ✓ 2M requests/month free           │
│  ✓ Auto-scaling 0-10 instances      │
└──────────────┬──────────────────────┘
               │ Private Connection
┌──────────────▼──────────────────────┐
│  Cloud SQL (PostgreSQL)             │
│  ✓ db-f1-micro free tier            │
│  ✓ 10GB storage free                │
└─────────────────────────────────────┘
```

---

## 📋 Application Screens

### Dashboard (Log Absence)
| Field | Type | Options |
|-------|------|---------|
| **Person** | Dropdown | From People list (Settings) |
| **Date** | Date Picker | Any date |
| **Duration** | Dropdown | First Half / Second Half / Full |
| **Type** | Dropdown | From Leave Types (Settings) |
| **Reason** | Text Area | Free text |

### Settings
- **People Tab**: Add, edit, delete team members
- **Leave Types Tab**: Manage leave categories (Annual, Medical, WFH, etc.)

---

## 🚀 Development Setup

### Prerequisites
- Python 3.11+
- Node.js 22+
- npm 11+

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run server
uvicorn app.main:app --reload
# Backend runs at: http://localhost:8000
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
# Frontend runs at: http://localhost:5173
```

### VS Code Launch (F5)
Press **F5** to launch both backend and frontend simultaneously!

---

## 📚 Documentation

### Getting Started
- **[QUICKSTART_ENV.md](./QUICKSTART_ENV.md)** - 3-minute quick start
- **[SETUP.md](./SETUP.md)** - Complete setup guide
- **[VERSION_1.0_RELEASE.md](./VERSION_1.0_RELEASE.md)** - Release notes

### Deployment
- **[QUICK_DEPLOY_GCP.md](./QUICK_DEPLOY_GCP.md)** - One-command deployment ⚡
- **[GOOGLE_CLOUD_DEPLOYMENT.md](./GOOGLE_CLOUD_DEPLOYMENT.md)** - Full GCP guide
- **[DEPLOY_SCRIPTS.md](./DEPLOY_SCRIPTS.md)** - Script documentation

### Configuration
- **[ENVIRONMENT_CONFIG.md](./ENVIRONMENT_CONFIG.md)** - Environment variables
- **[CONFIGURATION_SUMMARY.md](./CONFIGURATION_SUMMARY.md)** - Config details

### Architecture
- **[SECURITY_IMPLEMENTATION.md](./SECURITY_IMPLEMENTATION.md)** - JWT & API service
- **[frontend/PATH_ALIASES.md](./frontend/PATH_ALIASES.md)** - Import aliases
- **[JWT_IMPLEMENTATION.md](./JWT_IMPLEMENTATION.md)** - JWT details

---

## 🔐 Security Features

### Authentication
- **JWT Tokens**: 30-minute expiration with automatic refresh
- **HTTPBearer**: Secure token transmission
- **2FA**: TOTP-based (Google Authenticator)
- **Protected Endpoints**: All APIs require valid JWT

### Password Security
- **No Database Storage**: Passwords never stored
- **Custom Encryption**: Username encrypted with password-derived key (Fernet)
- **Password = Key**: Password acts as encryption key
- **No Recovery**: Cannot recover password (must recreate user)

### Environment Security
- **SECRET_KEY**: Randomly generated JWT signing key
- **Environment Variables**: All secrets in .env (not committed)
- **CORS**: Restricted to specific origins
- **HTTPS**: Enforced in production (Cloud Run)
---

## 💰 Deployment Costs

### Google Cloud Free Tier
Perfect for small to medium teams (up to 50 users):

| Service | Free Tier | Usage Estimate | Monthly Cost |
|---------|-----------|----------------|--------------|
| Cloud Run | 2M requests/month | ~100K requests | **$0** |
| Cloud SQL | db-f1-micro (1 CPU, 614MB RAM) | Small DB | **$0** |
| Cloud Storage | 5GB + 1GB egress | Frontend assets | **$0** |
| Artifact Registry | 0.5GB storage | Docker images | **$0** |
| **Total** | | | **$0/month** 🎉 |

**Note**: Exceeding free tier limits will incur charges. Set up budget alerts at $5/month.

---

## 🧪 Testing

### Manual Testing Checklist
- [ ] Registration with QR code generation
- [ ] Login with 2FA code from Google Authenticator
- [ ] JWT token stored in localStorage
- [ ] Dashboard loads people and types
- [ ] Log absence successfully
- [ ] Settings - Add/Edit/Delete person
- [ ] Settings - Add/Edit/Delete leave type
- [ ] Logout clears token
- [ ] 401 error on expired token
- [ ] Redirect to login when unauthenticated

### API Testing
```bash
# Access API docs
http://localhost:8000/docs

# Test registration
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"password123"}'

# Test login (after scanning QR)
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"password123","token":"123456"}'
```

---

## 📊 Project Structure

```
Leave-tracker-app/
├── backend/
│   ├── .env                    # Environment config (not committed)
│   ├── .env.example            # Environment template
│   ├── Dockerfile              # Docker configuration
│   ├── requirements.txt        # Python dependencies
│   └── app/
│       ├── main.py             # FastAPI application
│       ├── database.py         # Database setup
│       ├── models.py           # SQLAlchemy models
│       ├── schemas.py          # Pydantic schemas
│       ├── core/
│       │   └── security.py     # JWT + encryption
│       ├── api/
│       │   ├── auth.py         # Authentication
│       │   ├── people.py       # People management
│       │   ├── types.py        # Leave types
│       │   └── absences.py     # Absence logging
│       └── services/
│
├── frontend/
│   ├── .env.development        # Dev environment
│   ├── .env.production         # Prod environment
│   ├── tsconfig.app.json       # TypeScript config
│   ├── vite.config.ts          # Vite dev config
│   ├── vite.prod.config.ts     # Vite prod config
│   └── src/
│       ├── main.tsx            # Entry point
│       ├── App.tsx             # Main app component
│       ├── config.ts           # API configuration
│       ├── services/
│       │   └── api.ts          # API service layer
│       └── pages/
│           ├── Login.tsx       # Login page
│           ├── Register.tsx    # Registration page
│           ├── Dashboard.tsx   # Log absence form
│           └── Settings.tsx    # People & types management
│
├── .vscode/
│   └── launch.json             # F5 launch config
│
├── deploy-to-gcp.ps1           # Deployment script
├── README.md                   # This file
├── QUICK_DEPLOY_GCP.md         # Quick deployment guide
├── GOOGLE_CLOUD_DEPLOYMENT.md  # Full deployment guide
└── VERSION_1.0_RELEASE.md      # Release notes
```

---

## 🔄 Updating the Application

### Local Updates
```bash
# Make code changes
git add .
git commit -m "Updated feature X"
git push
```

### Deploy Updates to Google Cloud
```powershell
# Rebuild and deploy (increments version)
.\deploy-to-gcp.ps1 `
    -ProjectId "your-project-id" `
    -SecretKey "your-secret-key" `
    -DbPassword "your-db-password" `
    -Version "v1.0.1"
```

---

## 🐛 Troubleshooting

### Local Development

**Backend won't start?**
```bash
# Check Python version
python --version  # Should be 3.11+

# Verify dependencies
pip list | grep fastapi

# Check .env file exists
ls backend/.env
```

**Frontend won't start?**
```bash
# Check Node version
node --version  # Should be 22+

# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**JWT not working?**
```bash
# Check localStorage in browser DevTools
localStorage.getItem('access_token')

# Check Authorization header in Network tab
# Should be: Authorization: Bearer <token>
```

### Google Cloud Deployment

**Docker build fails?**
```powershell
# Ensure Docker Desktop is running
docker version

# Re-authenticate
gcloud auth login
gcloud auth configure-docker us-central1-docker.pkg.dev
```

**Backend deployment fails?**
```powershell
# Check logs
gcloud run services logs tail leave-tracker-api --region=us-central1

# Verify environment variables
gcloud run services describe leave-tracker-api --format=json
```

**Frontend 404 errors?**
```powershell
# Check bucket exists
gsutil ls gs://your-project-id-frontend

# Verify permissions
gsutil iam get gs://your-project-id-frontend
```

**CORS errors?**
```powershell
# Update CORS with exact frontend URL
gcloud run services update leave-tracker-api `
    --region=us-central1 `
    --update-env-vars="CORS_ORIGINS=https://storage.googleapis.com/your-bucket"
```

---

## 📈 Future Enhancements

### Planned for V2.0
- [ ] View absence history with filters
- [ ] Team calendar view
- [ ] Export to CSV/Excel
- [ ] Email notifications
- [ ] Manager approval workflow
- [ ] Role-based access control
- [ ] Absence balance tracking
- [ ] Dark mode theme
- [ ] Mobile responsive improvements
- [ ] Progressive Web App (PWA)

### Technical Improvements
- [ ] Unit tests (frontend & backend)
- [ ] Integration tests
- [ ] E2E tests (Playwright)
- [ ] API rate limiting
- [ ] Redis caching
- [ ] Database migrations (Alembic)
- [ ] CI/CD pipeline
- [ ] Kubernetes manifests

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern Python web framework
- **React** - UI library
- **Material-UI** - React component library
- **Google Cloud Platform** - Cloud hosting
- **pyotp** - 2FA implementation
- **python-jose** - JWT tokens

---

## 📞 Support

### Documentation
- [Quick Start Guide](./QUICKSTART_ENV.md)
- [Setup Instructions](./SETUP.md)
- [Deployment Guide](./GOOGLE_CLOUD_DEPLOYMENT.md)
- [Security Details](./SECURITY_IMPLEMENTATION.md)

### Issues
Found a bug? Have a feature request?
- Open an issue on GitHub
- Check existing documentation first
- Review logs: `gcloud run services logs tail leave-tracker-api`

---

## ⭐ Star This Repository

If you find this project helpful, please give it a star! ⭐

---

**Built with ❤️ using FastAPI, React, and Google Cloud Platform**

**Version 1.0** - Production Ready | [Release Notes](./VERSION_1.0_RELEASE.md)
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install
npm install @mui/material @emotion/react @emotion/styled axios
```

### 5️⃣ Example Login Page

`src/pages/Login.tsx`

```tsx
import { useState } from "react";
import axios from "axios";
import { TextField, Button, Card, Typography } from "@mui/material";

export default function Login() {
  const [username, setUsername] = useState("");
  const [token, setToken] = useState("");

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://localhost:8000/login", { username, token });
      alert(res.data.success ? "Login success!" : "Invalid 2FA token");
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <Card sx={{ p: 4, width: 300, mx: "auto", mt: 10 }}>
      <Typography variant="h6">2FA Login</Typography>
      <TextField label="Username" value={username} onChange={e => setUsername(e.target.value)} fullWidth margin="normal" />
      <TextField label="2FA Token" value={token} onChange={e => setToken(e.target.value)} fullWidth margin="normal" />
      <Button variant="contained" fullWidth onClick={handleLogin}>Login</Button>
    </Card>
  );
}
```

---

## 🧩 6️⃣ Google Cloud Deployment

### Steps:
1. Enable **Cloud Run**, **Cloud Build**, and **Artifact Registry**.
2. Create a `Dockerfile` inside `backend/`:

```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

3. Build and deploy:
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/team-tracker
gcloud run deploy team-tracker --image gcr.io/PROJECT-ID/team-tracker --platform managed --allow-unauthenticated
```

4. For frontend, you can host via:
   - Google Cloud Storage (Static Website)
   - Vercel / Netlify (recommended for free)

---

## 🧱 7️⃣ Key Endpoints

| Endpoint | Method | Description |
|-----------|--------|-------------|
| `/register` | POST | Register a user & return QR code for Google Authenticator |
| `/login` | POST | Verify username + 2FA token |
| `/people` | GET/POST | Manage team members |
| `/types` | GET/POST | Manage absence types |
| `/absences` | POST | Submit form data |

---

## 🕒 Estimated Time to Build

| Task | Time |
|------|------|
| Backend setup (FastAPI + DB + 2FA) | 2–3 hrs |
| Frontend setup (React + MUI + routing) | 2 hrs |
| Form UI + API integration | 2 hrs |
| Deployment on Cloud Run & Storage | 1 hr |
| **Total** | **~1 day max** |

---

## ✅ Summary

You’ll get a simple but production-ready **attendance tracker** app where:
- You log in securely via 2FA.
- Submit absences or WFH notices.
- Manage dropdown options dynamically.
- Deploy for **free on Google Cloud Run** + **React hosted frontend**.

---

**Next Step:**  
Would you like me to generate the actual FastAPI + React folder structure with base files as a ready-to-run zip package?
