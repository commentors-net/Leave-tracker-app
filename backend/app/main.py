from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth, people, types, absences

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(people.router, prefix="/api", tags=["people"])
app.include_router(types.router, prefix="/api", tags=["types"])
app.include_router(absences.router, prefix="/api", tags=["absences"])