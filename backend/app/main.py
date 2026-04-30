from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from app.database import engine, Base
import app.models

from app.routes import user, payments

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FixIt API")

# ======================
# CORS CONFIG (IMPORTANT)
# ======================
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://your-frontend-url.onrender.com"  # 🔥 REPLACE THIS
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # ✅ safer than "*"
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