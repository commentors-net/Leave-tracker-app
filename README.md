# 🧭 Leave Tracker - Team Absence Management# 🧭 Leave Tracker - Team Absence Management



**Version 1.1.0** | A **production-ready web application** for managing team absences with AI-powered features.A **production-ready web application** built with **FastAPI (Python)** backend and **React (TypeScript)** frontend.  

Features secure **JWT authentication with 2FA**, comprehensive leave management, and **one-command deployment to Google Cloud (Free Tier)**.

Built with **FastAPI (Python)** + **React (TypeScript)** + **Google Cloud (100% Free Tier)**

---

---

## 🎯 Quick Start

## 🎯 Quick Start

### 🏃 Local Development

### 📖 Complete Documentation```powershell

# Press F5 in VS Code (both backend + frontend launch)

**👉 [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)** - Everything you need:# Or manually:

- ✅ Architecture & setup instructionscd backend; uvicorn app.main:app --reload

- ✅ Feature implementation details  cd frontend; npm run dev

- ✅ Security best practices```

- ✅ Complete API reference

- ✅ Google Cloud deployment guide### ☁️ Deploy to Google Cloud (FREE)

- ✅ Configuration management```powershell

- ✅ Troubleshooting & maintenance# One command deployment!

.\deploy-to-gcp.ps1 `

### 🏃 Local Development (30 seconds)    -ProjectId "your-project-id" `

    -SecretKey "$(python -c 'import secrets; print(secrets.token_hex(32))')" `

```powershell    -DbPassword "your-secure-password"

# Backend```

cd backend**See**: [QUICK_DEPLOY_GCP.md](./QUICK_DEPLOY_GCP.md) | [Full Guide](./GOOGLE_CLOUD_DEPLOYMENT.md)

python -m venv venv

.\venv\Scripts\activate---

pip install -r requirements.txt

uvicorn app.main:app --reload## ✨ Features



# Frontend (new terminal)### Core Functionality

cd frontend- 🔐 **Secure Authentication**: JWT tokens with 30-minute expiration

npm install- 🔑 **2FA**: Google Authenticator integration with QR codes

npm run dev- 👥 **People Management**: Add, edit, delete team members

```- � **Leave Types**: Customizable leave categories

- 📅 **Absence Logging**: Track leaves with date, duration, type, reason

**Or press F5 in VS Code** - launches both backend + frontend automatically!- ⚙️ **Settings Interface**: Tabbed UI for managing people and types

- 🎨 **Modern UI**: Material-UI components with responsive design

### ☁️ Deploy to Google Cloud (15 minutes, FREE)

### Technical Features

```powershell- 🔒 **Custom Password Encryption**: Username encrypted with password-derived key

.\deploy-to-gcp.ps1 `- 🛡️ **JWT Protection**: All API endpoints secured

    -ProjectId "leave-tracker-2025" `- 🔄 **Automatic Token Handling**: Axios interceptors for seamless auth

    -SecretKey "$(python -c 'import secrets; print(secrets.token_hex(32))')" `- 📁 **Path Aliases**: Clean imports (`@services/api`)

    -DbPassword "your-secure-password" `- 🌐 **Environment Config**: Separate dev/prod configurations

    -GeminiApiKey "your-gemini-api-key"- � **Docker Ready**: Containerized backend for easy deployment

```- ☁️ **Cloud Native**: Optimized for Google Cloud Run + Cloud SQL



**Cost**: $0/month (all within free tier limits)---



---## 🏗️ Architecture



## ✨ Features### Tech Stack

```

### 🔐 Authentication & Security┌─────────────────────────────────────┐

- **JWT Tokens** with 30-minute expiration│  Frontend (React 19 + TypeScript)   │

- **2FA (TOTP)** using Google Authenticator│  - Material-UI 7                    │

- **Custom Encryption** - Username encrypted with password-derived key│  - React Router 7                   │

- **Protected API** - All endpoints secured with JWT│  - Axios with JWT interceptors      │

- **Registration Control** - Enable/disable public registration│  - Path aliases (@services/*)       │

└──────────────┬──────────────────────┘

### 📋 Leave Management               │ REST API (JWT Bearer)

- **People Management** - Add, edit, delete team members┌──────────────▼──────────────────────┐

- **Leave Types** - Customizable categories (Medical, Annual, WFH, etc.)│  Backend (FastAPI + Python 3.11)    │

- **Absence Logging** - Track date, duration, type, reason│  - SQLAlchemy ORM                   │

- **Settings Interface** - Clean tabbed UI for configuration│  - JWT Authentication               │

│  - Custom Password Encryption       │

### 🤖 Smart Identification (NEW in v1.1.0)│  - 2FA (TOTP/Google Authenticator)  │

- **AI-Powered Parsing** - Automatically extract leave info from chat conversations└──────────────┬──────────────────────┘

- **Google Gemini Integration** - Free tier (15 req/min, 1M tokens/day)               │

- **Multi-Format Support** - WhatsApp, Telegram, Slack, Teams┌──────────────▼──────────────────────┐

- **Smart Name Matching** - Auto-map detected names to database people│  Database                            │

- **Confidence Scoring** - High/Medium/Low indicators│  - SQLite (local dev)               │

- **Batch Processing** - Save individual or all entries at once│  - PostgreSQL (production/GCP)      │

└─────────────────────────────────────┘

### 🛠️ Technical Highlights```

- **Modern Stack** - React 19, TypeScript 5, FastAPI, PostgreSQL 14

- **Material-UI** - Beautiful, responsive components### Google Cloud Deployment

- **Path Aliases** - Clean imports (`@services/api`, `@pages/Login`)```

- **Docker Ready** - Backend containerization┌─────────────────────────────────────┐

- **Cloud Native** - Optimized for Google Cloud Run + Cloud SQL│  Cloud Storage + CDN (Frontend)     │

- **Environment Config** - Separate dev/prod settings│  ✓ 5GB storage free                 │

- **Automatic Token Handling** - Axios interceptors│  ✓ 1GB egress free                  │

└─────────────────────────────────────┘

---               │ HTTPS

┌──────────────▼──────────────────────┐

## 🏗️ Architecture│  Cloud Run (Backend API)            │

│  ✓ 2M requests/month free           │

```│  ✓ Auto-scaling 0-10 instances      │

┌────────────────────────────────────────────┐└──────────────┬──────────────────────┘

│  Frontend (React + TypeScript)              │               │ Private Connection

│  Cloud Storage - Static Website Hosting    │┌──────────────▼──────────────────────┐

│  - Material-UI components                  ││  Cloud SQL (PostgreSQL)             │

│  - JWT token management                    ││  ✓ db-f1-micro free tier            │

│  - Smart Identification UI                 ││  ✓ 10GB storage free                │

└────────────────┬───────────────────────────┘└─────────────────────────────────────┘

                 │ HTTPS/REST API```

┌────────────────▼───────────────────────────┐

│  Backend (FastAPI + Python)                │---

│  Cloud Run - Serverless Containers         │

│  - JWT + 2FA authentication                │## 📋 Application Screens

│  - Google Gemini AI integration            │

│  - SQLAlchemy ORM                          │### Dashboard (Log Absence)

└────────────────┬───────────────────────────┘| Field | Type | Options |

                 │ Cloud SQL Proxy|-------|------|---------|

┌────────────────▼───────────────────────────┐| **Person** | Dropdown | From People list (Settings) |

│  Database (PostgreSQL)                     │| **Date** | Date Picker | Any date |

│  Cloud SQL - Managed Database              │| **Duration** | Dropdown | First Half / Second Half / Full |

│  - db-f1-micro (Free Tier)                 │| **Type** | Dropdown | From Leave Types (Settings) |

│  - Automatic backups                       │| **Reason** | Text Area | Free text |

└────────────────────────────────────────────┘

```### Settings

- **People Tab**: Add, edit, delete team members

---- **Leave Types Tab**: Manage leave categories (Annual, Medical, WFH, etc.)



## 📦 Tech Stack---



| Layer | Technology | Version |## 🚀 Development Setup

|-------|------------|---------|

| **Frontend** | React | 19.x |### Prerequisites

| | TypeScript | 5.x |- Python 3.11+

| | Material-UI | 6.x |- Node.js 22+

| | Vite | 7.x |- npm 11+

| **Backend** | Python | 3.11+ |

| | FastAPI | Latest |### Backend Setup

| | SQLAlchemy | Latest |```bash

| | Google Gemini AI | Latest |cd backend

| **Database** | PostgreSQL | 14+ |

| | SQLite | (dev only) |# Create virtual environment

| **Hosting** | Google Cloud Run | Serverless |python -m venv venv

| | Cloud SQL | Managed DB |.\venv\Scripts\activate  # Windows

| | Cloud Storage | Static site |source venv/bin/activate  # Mac/Linux

| **Tools** | Docker | Containers |

| | gcloud CLI | Deployment |# Install dependencies

| | VS Code | IDE (F5 debug) |pip install -r requirements.txt



---# Create .env file

cp .env.example .env

## 📂 Project Structure

# Run server

```uvicorn app.main:app --reload

Leave-tracker-app/# Backend runs at: http://localhost:8000

├── backend/```

│   ├── app/

│   │   ├── main.py                    # FastAPI entry point### Frontend Setup

│   │   ├── database.py                # Database connection```bash

│   │   ├── models.py                  # SQLAlchemy modelscd frontend

│   │   ├── schemas.py                 # Pydantic schemas

│   │   ├── core/# Install dependencies

│   │   │   └── security.py            # JWT + encryptionnpm install

│   │   ├── api/

│   │   │   ├── auth.py                # Authentication# Run dev server

│   │   │   ├── people.py              # People CRUDnpm run dev

│   │   │   ├── types.py               # Leave types CRUD# Frontend runs at: http://localhost:5173

│   │   │   ├── absences.py            # Absences CRUD```

│   │   │   └── smart_identification.py # AI parsing

│   │   └── services/### VS Code Launch (F5)

│   ├── DockerfilePress **F5** to launch both backend and frontend simultaneously!

│   └── requirements.txt

│---

├── frontend/

│   ├── src/## 📚 Documentation

│   │   ├── main.tsx                   # React entry point

│   │   ├── App.tsx                    # Main app + routing### Getting Started

│   │   ├── config.ts                  # API configuration- **[QUICKSTART_ENV.md](./QUICKSTART_ENV.md)** - 3-minute quick start

│   │   ├── pages/- **[SETUP.md](./SETUP.md)** - Complete setup guide

│   │   │   ├── Login.tsx- **[VERSION_1.0_RELEASE.md](./VERSION_1.0_RELEASE.md)** - Release notes

│   │   │   ├── Register.tsx

│   │   │   ├── Dashboard.tsx### Deployment

│   │   │   ├── Settings.tsx- **[QUICK_DEPLOY_GCP.md](./QUICK_DEPLOY_GCP.md)** - One-command deployment ⚡

│   │   │   └── SmartIdentification.tsx # AI parsing UI- **[GOOGLE_CLOUD_DEPLOYMENT.md](./GOOGLE_CLOUD_DEPLOYMENT.md)** - Full GCP guide

│   │   └── services/- **[DEPLOY_SCRIPTS.md](./DEPLOY_SCRIPTS.md)** - Script documentation

│   │       └── api.ts                 # API client

│   ├── package.json### Configuration

│   └── vite.config.ts- **[ENVIRONMENT_CONFIG.md](./ENVIRONMENT_CONFIG.md)** - Environment variables

│- **[CONFIGURATION_SUMMARY.md](./CONFIGURATION_SUMMARY.md)** - Config details

├── deploy-frontend.ps1                # Frontend deployment

├── deploy-to-gcp.ps1                  # Full GCP deployment### Architecture

├── DEVELOPER_GUIDE.md                 # Complete documentation- **[SECURITY_IMPLEMENTATION.md](./SECURITY_IMPLEMENTATION.md)** - JWT & API service

└── README.md                          # This file- **[frontend/PATH_ALIASES.md](./frontend/PATH_ALIASES.md)** - Import aliases

```- **[JWT_IMPLEMENTATION.md](./JWT_IMPLEMENTATION.md)** - JWT details



------



## 🚀 Getting Started## 🔐 Security Features



### Prerequisites### Authentication

- **JWT Tokens**: 30-minute expiration with automatic refresh

- **Python 3.11+** - Backend runtime- **HTTPBearer**: Secure token transmission

- **Node.js 18+** - Frontend build tool- **2FA**: TOTP-based (Google Authenticator)

- **Google Cloud Account** - For deployment (free tier)- **Protected Endpoints**: All APIs require valid JWT

- **Gemini API Key** - For Smart Identification (free)

### Password Security

### 1. Clone Repository- **No Database Storage**: Passwords never stored

- **Custom Encryption**: Username encrypted with password-derived key (Fernet)

```powershell- **Password = Key**: Password acts as encryption key

git clone https://github.com/commentors-net/Leave-tracker-app.git- **No Recovery**: Cannot recover password (must recreate user)

cd Leave-tracker-app

```### Environment Security

- **SECRET_KEY**: Randomly generated JWT signing key

### 2. Local Setup- **Environment Variables**: All secrets in .env (not committed)

- **CORS**: Restricted to specific origins

**Backend**:- **HTTPS**: Enforced in production (Cloud Run)

```powershell---

cd backend

python -m venv venv## 💰 Deployment Costs

.\venv\Scripts\activate

pip install -r requirements.txt### Google Cloud Free Tier

Perfect for small to medium teams (up to 50 users):

# Create .env file

@"| Service | Free Tier | Usage Estimate | Monthly Cost |

SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")|---------|-----------|----------------|--------------|

DATABASE_URL=sqlite:///./database.db| Cloud Run | 2M requests/month | ~100K requests | **$0** |

CORS_ORIGINS=http://localhost:5173| Cloud SQL | db-f1-micro (1 CPU, 614MB RAM) | Small DB | **$0** |

GEMINI_API_KEY=your_key_here| Cloud Storage | 5GB + 1GB egress | Frontend assets | **$0** |

"@ | Out-File -FilePath .env -Encoding utf8| Artifact Registry | 0.5GB storage | Docker images | **$0** |

| **Total** | | | **$0/month** 🎉 |

uvicorn app.main:app --reload

```**Note**: Exceeding free tier limits will incur charges. Set up budget alerts at $5/month.



**Frontend**:---

```powershell

cd frontend## 🧪 Testing

npm install

### Manual Testing Checklist

# Create .env.development- [ ] Registration with QR code generation

@"- [ ] Login with 2FA code from Google Authenticator

VITE_API_URL=http://localhost:8000- [ ] JWT token stored in localStorage

VITE_ENABLE_REGISTRATION=true- [ ] Dashboard loads people and types

"@ | Out-File -FilePath .env.development -Encoding utf8- [ ] Log absence successfully

- [ ] Settings - Add/Edit/Delete person

npm run dev- [ ] Settings - Add/Edit/Delete leave type

```- [ ] Logout clears token

- [ ] 401 error on expired token

### 3. First Time Setup- [ ] Redirect to login when unauthenticated



1. Go to http://localhost:5173/register### API Testing

2. Create account and scan QR code with Google Authenticator```bash

3. Login with username + password + 2FA code# Access API docs

4. Go to Settings → Add people and leave typeshttp://localhost:8000/docs

5. Test Smart Identification with example conversation

# Test registration

### 4. Deploy to Google Cloudcurl -X POST "http://localhost:8000/auth/register" \

  -H "Content-Type: application/json" \

See **[DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)** for complete deployment instructions.  -d '{"username":"test","password":"password123"}'



---# Test login (after scanning QR)

curl -X POST "http://localhost:8000/auth/login" \

## 🔐 Security Features  -H "Content-Type: application/json" \

  -d '{"username":"test","password":"password123","token":"123456"}'

- ✅ **JWT Authentication** - 30-minute token expiration```

- ✅ **2FA (TOTP)** - Google Authenticator integration

- ✅ **Password Encryption** - Username encrypted with password-derived key---

- ✅ **Endpoint Protection** - All API routes require valid JWT

- ✅ **CORS Configuration** - Restricted to frontend domain## 📊 Project Structure

- ✅ **HTTPS Enforced** - Cloud Run provides automatic SSL

- ✅ **SQL Injection Protection** - SQLAlchemy ORM parameterization```

- ✅ **XSS Protection** - React escapes output by defaultLeave-tracker-app/

├── backend/

---│   ├── .env                    # Environment config (not committed)

│   ├── .env.example            # Environment template

## 💰 Cost Breakdown (Free Tier)│   ├── Dockerfile              # Docker configuration

│   ├── requirements.txt        # Python dependencies

| Service | Configuration | Free Tier Limit | Monthly Cost |│   └── app/

|---------|---------------|-----------------|--------------|│       ├── main.py             # FastAPI application

| **Cloud Run** | 512Mi RAM, 1 CPU | 2M requests/month | **$0** |│       ├── database.py         # Database setup

| **Cloud SQL** | db-f1-micro, 10GB | 1 instance | **$0** |│       ├── models.py           # SQLAlchemy models

| **Cloud Storage** | Website hosting | 5GB + 1GB egress | **$0** |│       ├── schemas.py          # Pydantic schemas

| **Artifact Registry** | Docker images | 0.5GB | **$0** |│       ├── core/

| **Cloud Build** | Remote builds | 120 min/day | **$0** |│       │   └── security.py     # JWT + encryption

| **Gemini API** | 1.5 Flash | 15 req/min, 1M tokens/day | **$0** |│       ├── api/

| **TOTAL** | Small team usage | All within limits | **$0/month** |│       │   ├── auth.py         # Authentication

│       │   ├── people.py       # People management

---│       │   ├── types.py        # Leave types

│       │   └── absences.py     # Absence logging

## 📖 Documentation│       └── services/

│

- **[DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)** - Complete guide (2000+ lines)├── frontend/

  - Architecture & data flow│   ├── .env.development        # Dev environment

  - Local development setup│   ├── .env.production         # Prod environment

  - Feature implementation details│   ├── tsconfig.app.json       # TypeScript config

  - Security best practices│   ├── vite.config.ts          # Vite dev config

  - Complete API reference│   ├── vite.prod.config.ts     # Vite prod config

  - Google Cloud deployment (step-by-step)│   └── src/

  - Configuration management│       ├── main.tsx            # Entry point

  - Troubleshooting guide│       ├── App.tsx             # Main app component

  - Maintenance & updates│       ├── config.ts           # API configuration

│       ├── services/

---│       │   └── api.ts          # API service layer

│       └── pages/

## 🤝 Contributing│           ├── Login.tsx       # Login page

│           ├── Register.tsx    # Registration page

1. Fork the repository│           ├── Dashboard.tsx   # Log absence form

2. Create feature branch (`git checkout -b feature/amazing-feature`)│           └── Settings.tsx    # People & types management

3. Commit changes (`git commit -m 'Add amazing feature'`)│

4. Push to branch (`git push origin feature/amazing-feature`)├── .vscode/

5. Open Pull Request│   └── launch.json             # F5 launch config

│

---├── deploy-to-gcp.ps1           # Deployment script

├── README.md                   # This file

## 📝 License├── QUICK_DEPLOY_GCP.md         # Quick deployment guide

├── GOOGLE_CLOUD_DEPLOYMENT.md  # Full deployment guide

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.└── VERSION_1.0_RELEASE.md      # Release notes

```

---

---

## 🔗 Links

## 🔄 Updating the Application

- **Live Demo**: https://storage.googleapis.com/leave-tracker-2025-frontend/index.html

- **API Docs**: https://leave-tracker-api-427212681311.us-central1.run.app/docs### Local Updates

- **Google Cloud Console**: https://console.cloud.google.com/home/dashboard?project=leave-tracker-2025```bash

- **Gemini API**: https://makersuite.google.com/app/apikey# Make code changes

git add .

---git commit -m "Updated feature X"

git push

## 📞 Support```



For detailed help, see **[DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)** sections:### Deploy Updates to Google Cloud

- **Troubleshooting** - Common issues and solutions```powershell

- **Configuration** - Environment variables guide# Rebuild and deploy (increments version)

- **API Reference** - Complete endpoint documentation.\deploy-to-gcp.ps1 `

- **Deployment** - Step-by-step GCP setup    -ProjectId "your-project-id" `

    -SecretKey "your-secret-key" `

---    -DbPassword "your-db-password" `

    -Version "v1.0.1"

**Version**: 1.1.0  ```

**Last Updated**: November 2, 2025  

**Status**: ✅ Production Ready---


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
