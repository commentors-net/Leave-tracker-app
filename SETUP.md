# Running the Leave Tracker Application

This guide explains how to run the Leave Tracker application locally for development and testing.

## Prerequisites

- Python 3.11 or higher (tested with Python 3.11.6)
- Node.js 22 or higher (tested with Node.js 22.12.0)
- npm 11 or higher (tested with npm 11.6.1)

## Backend Setup

### 1. Navigate to the backend directory

```bash
cd backend
```

### 2. Create and activate a virtual environment

**On Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the backend server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend API will be available at `http://localhost:8000`

API documentation (Swagger UI) will be available at `http://localhost:8000/docs`

### 5. Seed initial data (optional)

Before using the application, you may want to add some initial leave types. You can do this via the API or the Settings page in the frontend.

Default leave types to add:
- Annual Leave
- Medical Leave
- Medical Dependent Leave
- Work From Home (WFH)

## Frontend Setup

### 1. Navigate to the frontend directory

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start the development server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173` (or another port if 5173 is in use)

## Using the Application

### First Time Setup

1. **Register a User**
   - Navigate to `http://localhost:5173/register`
   - Enter a username and password
   - A QR code will be displayed
   - Scan this QR code with Google Authenticator or another 2FA app
   - Save your username and 2FA secret

2. **Setup People and Leave Types**
   - Navigate to Settings (`http://localhost:5173/settings`)
   - Add team members under "Manage People"
   - Add leave types (Annual, Medical, Medical Dependent, WFH, etc.) under "Manage Leave Types"

3. **Login**
   - Navigate to Login page
   - Enter your username
   - Enter the 6-digit code from your 2FA app
   - Click Login

4. **Log Absences**
   - Navigate to Dashboard
   - Fill in the form:
     - Select a person
     - Choose a date
     - Select duration (First Half, Second Half, Full Day)
     - Select leave type
     - Add a reason
   - Click Submit

## Building for Production

### Backend

Build a Docker image:
```bash
cd backend
docker build -t leave-tracker-backend .
docker run -p 8080:8080 leave-tracker-backend
```

### Frontend

Build the production bundle:
```bash
cd frontend
npm run build
```

The built files will be in the `dist` directory and can be served with any static file server or hosted on platforms like Vercel, Netlify, or Google Cloud Storage.

## Troubleshooting

### Backend won't start
- Ensure Python 3.11+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify no other process is using port 8000

### Frontend won't start
- Ensure Node.js 22+ is installed
- Delete `node_modules` and `package-lock.json`, then run `npm install` again
- Check that no other process is using port 5173

### Can't connect to backend from frontend
- Ensure backend is running on port 8000
- Check CORS settings in `backend/app/main.py`
- Verify the API URL in frontend components is correct (`http://localhost:8000`)

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/register` | POST | Register a new user with 2FA |
| `/auth/login` | POST | Login with username and 2FA token |
| `/api/people` | GET | List all people |
| `/api/people` | POST | Add a new person |
| `/api/types` | GET | List all leave types |
| `/api/types` | POST | Add a new leave type |
| `/api/absences` | GET | List all absences |
| `/api/absences` | POST | Log a new absence |

## Environment Variables

The application uses environment variables for configuration. Example files (`.env.example`) are provided - copy them to create your own `.env` files.

### Backend Environment Configuration

1. **Copy the example file:**
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Configure the following variables in `backend/.env`:**

   | Variable | Description | Default | Required |
   |----------|-------------|---------|----------|
   | `SECRET_KEY` | JWT token signing key (use a strong random key) | Generated value | Yes |
   | `ALGORITHM` | JWT algorithm | HS256 | No |
   | `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration time | 30 | No |
   | `DATABASE_URL` | Database connection string | sqlite:///./database.db | No |
   | `PORT` | Server port | 8000 | No |
   | `HOST` | Server host | 0.0.0.0 | No |
   | `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | http://localhost:5173,http://localhost:3000 | No |

3. **Generate a secure SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copy the output and replace the `SECRET_KEY` value in `.env`

### Frontend Environment Configuration

1. **For Development:**
   - The `.env.development` file is already configured with `VITE_API_URL=http://localhost:8000`
   - No changes needed for local development

2. **For Production:**
   - Copy `.env.production` to `.env.production.local` (optional)
   - Update `VITE_API_URL` to your production backend URL:
     ```bash
     VITE_API_URL=https://your-production-api.com
     ```

3. **Environment Files Priority:**
   - `.env.local` - loaded in all cases, ignored by git
   - `.env.development` - loaded in development mode
   - `.env.production` - loaded in production mode
   - `.env` - loaded in all cases

### Security Notes

⚠️ **Important:**
- Never commit `.env` files to version control
- The `.gitignore` file is configured to exclude `.env` files
- Always use strong, randomly generated values for `SECRET_KEY`
- In production, use environment-specific secrets management (e.g., Google Cloud Secret Manager)
- Rotate your `SECRET_KEY` periodically in production

### Environment Variable Reference

**Backend (.env):**
```env
# JWT Configuration
SECRET_KEY=your-secret-key-change-this-in-production-use-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
DATABASE_URL=sqlite:///./database.db

# Server Configuration
PORT=8000
HOST=0.0.0.0

# CORS Configuration (comma-separated origins)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

**Frontend (.env.development):**
```env
VITE_API_URL=http://localhost:8000
```

**Frontend (.env.production):**
```env
VITE_API_URL=https://your-production-api.com
```

