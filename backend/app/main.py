from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from app.database import engine, Base
import app.models

from app.routes import user, payments

app = FastAPI(title="FixIt API")

# ======================
# CREATE TABLES ON STARTUP (FIXED)
# ======================
@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print("❌ Error creating tables:", e)

# ======================
# CORS CONFIG
# ======================
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://fixit-frontend-r16u.onrender.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# ROUTES
# ======================
app.include_router(user.router)
app.include_router(payments.router)

# ======================
# ROOT TEST
# ======================
@app.get("/")
def root():
    return {"message": "🚀 FixIt API is running"}