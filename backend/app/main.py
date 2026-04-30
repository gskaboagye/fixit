from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.database import engine, Base
import app.models

from app.routes import user, payments

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FixIt API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES
app.include_router(user.router)
app.include_router(payments.router)

@app.get("/")
def root():
    return {"message": "🚀 FixIt API is running"}