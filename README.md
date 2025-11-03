# 🧭 Leave Tracker - Team Absence Management

**Version 1.2.0** | Production-ready team leave tracking application

A modern web application for managing team absences with secure authentication, AI-powered leave parsing, and seamless deployment to Google Cloud Platform.

---

## 📖 What is Leave Tracker?

Leave Tracker helps teams manage employee absences efficiently with:

- **🔐 Secure Authentication** - JWT tokens with 2FA (TOTP/Google Authenticator)
- **👥 People Management** - Track team members and their information
- **📋 Leave Types** - Customizable categories (Medical, Annual, WFH, Dependent, etc.)
- **📅 Absence Logging** - Record leaves with date, duration, type, and reason
- **🤖 AI-Powered Parsing** - Smart Identification feature using Google Gemini to extract leave requests from chat conversations (WhatsApp, Slack, Teams)
- **📊 Reports & Analytics** - View and manage all absence records
- **⚙️ Settings Management** - Easy configuration of people and leave types

---

## 🚀 Technology Stack

### Backend
- **FastAPI** (Python 3.11+) - Modern async web framework
- **Firestore** (Production) - Cloud-native NoSQL database
- **SQLite** (Development) - Lightweight local database
- **JWT + TOTP** - Secure authentication with 2FA
- **Google Gemini API** - AI-powered leave identification
- **Docker** - Containerized deployment

### Frontend
- **React 19** - Modern UI framework
- **TypeScript** - Type-safe development
- **Material-UI 6** - Professional component library
- **Vite 7** - Lightning-fast build tool
- **Axios** - HTTP client with interceptors

### Cloud Infrastructure
- **Google Cloud Run** - Serverless backend hosting
- **Google Firestore** - Managed NoSQL database
- **Google Cloud Storage** - Frontend static hosting
- **Google Cloud Build** - Automated CI/CD

---

## 🎯 Quick Start

### For Developers

See **[DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)** for complete documentation:
- ✅ Local development setup
- ✅ Architecture and design patterns
- ✅ Database abstraction layer (SQLite/Firestore)
- ✅ Feature implementation details
- ✅ Security best practices
- ✅ API reference
- ✅ Deployment guides
- ✅ Troubleshooting

### Local Development (2 minutes)

```powershell
# Clone repository
git clone https://github.com/commentors-net/Leave-tracker-app.git
cd Leave-tracker-app

# Backend setup
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
# Press F5 in VS Code or run:
uvicorn app.main:app --reload

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev

# Access application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Deploy to Google Cloud (FREE)

```powershell
.\deploy-backend-update.ps1

# Or full deployment:
.\deploy-to-gcp-complete.ps1 `
  -ProjectId "your-project-id" `
  -SecretKey "$(python -c 'import secrets; print(secrets.token_hex(32))')" `
  -DbPassword "your-secure-password" `
  -GeminiApiKey "your-gemini-api-key"
```

**Cost**: $0/month (all within free tier limits)

---

## ✨ Key Features

### Core Features
- ✅ JWT authentication with 30-minute token expiration
- ✅ 2FA using Google Authenticator (TOTP)
- ✅ People management (add, edit, delete team members)
- ✅ Leave types management (customizable categories)
- ✅ Absence logging with date, duration, type, reason
- ✅ Reports and analytics dashboard
- ✅ Settings interface for configuration

### Advanced Features
- ✅ **Smart Identification** - AI-powered chat conversation parsing
  - Supports WhatsApp, Slack, Teams, Telegram formats
  - Automatically extracts person, date, leave type, reason
  - Confidence scoring and review interface
  - Batch processing and save
- ✅ **Database Abstraction** - Seamless switch between SQLite (dev) and Firestore (prod)
- ✅ **Registration Control** - Enable/disable public registration
- ✅ **Secure Password Handling** - Username encrypted with password-derived key
- ✅ **Automatic Token Management** - Axios interceptors handle JWT seamlessly
- ✅ **Path Aliases** - Clean imports using `@services/api`, `@pages/`

### Security Features
- 🔒 Custom password encryption with PBKDF2
- 🛡️ JWT protection on all API endpoints
- 🔄 Automatic token refresh and expiration handling
- 📁 Environment-based configuration
- 🌐 CORS configuration for secure cross-origin requests
- 🔐 2FA mandatory for all users

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| **[DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)** | Complete guide for developers - setup, architecture, features, deployment |
| **[LICENSE](./LICENSE)** | MIT License |

---

## 🏗️ Project Structure

```
Leave-tracker-app/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Security & utilities
│   │   ├── db_factory.py # Database abstraction
│   │   ├── sqlite_db.py  # SQLite implementation
│   │   └── firestore_db.py # Firestore implementation
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/             # React frontend
│   ├── src/
│   │   ├── pages/       # UI pages
│   │   ├── services/    # API client
│   │   └── config.ts    # Configuration
│   ├── package.json
│   └── vite.config.ts
├── deploy-backend-update.ps1 # Backend deployment
├── DEVELOPER_GUIDE.md    # Complete documentation
└── README.md            # This file
```

---

## 💰 Cost Estimate

### Free Tier (Google Cloud)
- **Cloud Run**: 2M requests/month
- **Firestore**: 50K reads, 20K writes, 20K deletes per day
- **Cloud Storage**: 5GB storage + 1GB egress/month
- **Gemini API**: 15 requests/min, 1M tokens/day

### Expected Monthly Cost
- **Small team (< 20 people)**: **$0/month**
- **All services within free tier limits**

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Repository**: https://github.com/commentors-net/Leave-tracker-app
- **Issues**: https://github.com/commentors-net/Leave-tracker-app/issues
- **Gemini API Key**: https://aistudio.google.com/apikey
- **Google Cloud Console**: https://console.cloud.google.com

---

## 📧 Support

For detailed documentation, troubleshooting, and development guides, see **[DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md)**.

For issues or questions:
1. Check the [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md) troubleshooting section
2. Review backend/frontend logs
3. Create a GitHub issue with details

---

**Version**: 1.2.0  
**Last Updated**: November 3, 2025  
**Status**: Production Ready ✅
