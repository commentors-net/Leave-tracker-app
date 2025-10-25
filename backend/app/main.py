import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .api import auth, people, types, absences

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS from environment variable
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(people.router, prefix="/api", tags=["people"])
app.include_router(types.router, prefix="/api", tags=["types"])
app.include_router(absences.router, prefix="/api", tags=["absences"])