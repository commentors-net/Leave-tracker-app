# Running the Leave Tracker Application

This guide explains how to run the Leave Tracker application locally for development and testing.

## Prerequisites

- Python 3.10 or higher
- Node.js 16 or higher
- npm or yarn

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
- Ensure Python 3.10+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify no other process is using port 8000

### Frontend won't start
- Ensure Node.js 16+ is installed
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

Currently, the application uses default configurations. For production:

### Backend
- `DATABASE_URL`: SQLite database path (default: `sqlite:///./database.db`)
- `PORT`: Server port (default: 8080 for Docker, 8000 for local)

### Frontend
- `VITE_API_URL`: Backend API URL (default: `http://localhost:8000`)

To use custom environment variables, create `.env` files:
- Backend: Create `.env` in the `backend` directory
- Frontend: Create `.env` in the `frontend` directory
