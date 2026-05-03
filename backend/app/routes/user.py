from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app import schemas
from app.database import get_db
from app.security import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password
)
from app.models import User, ChatMessage, Review, TechnicianLocation

router = APIRouter()


# ======================
# AUTH
# ======================

@router.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # 🔥 check duplicate email
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        password=hash_password(user.password),  # 🔥 FIX
        role="user"  # 🔥 FORCE DEFAULT
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 🔥 VERY IMPORTANT FIX
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {   # 🔥 helps frontend
            "id": db_user.id,
            "email": db_user.email,
            "role": db_user.role
        }
    }


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return current_user


# ======================
# REQUESTS
# ======================

@router.post("/requests")
def create_request(
    request: schemas.ServiceRequestCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "user":
        raise HTTPException(status_code=403, detail="Only users allowed")

    return crud.create_request(db, request, current_user.id)


@router.get("/requests")
def get_requests(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_requests(db, current_user.id)


# ======================
# TECHNICIAN JOBS
# ======================

@router.get("/technician/jobs")
def get_jobs(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "technician":
        raise HTTPException(status_code=403, detail="Only technicians")

    return crud.get_technician_jobs(db, current_user.id)


# ======================
# CHAT 💬
# ======================

@router.post("/chat/send")
def send_message(
    request_id: int,
    message: str,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = ChatMessage(
        request_id=request_id,
        sender_id=current_user.id,
        message=message
    )

    db.add(chat)
    db.commit()

    return {"message": "Message sent"}


@router.get("/chat/{request_id}")
def get_messages(request_id: int, db: Session = Depends(get_db)):
    return db.query(ChatMessage).filter(
        ChatMessage.request_id == request_id
    ).all()


# ======================
# REVIEWS ⭐
# ======================

@router.post("/reviews")
def create_review(
    request_id: int,
    technician_id: int,
    rating: int,
    comment: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    review = Review(
        request_id=request_id,
        technician_id=technician_id,
        rating=rating,
        comment=comment
    )

    db.add(review)
    db.commit()

    return {"message": "Review submitted"}


# ======================
# LIVE TRACKING 📍
# ======================

@router.post("/tracking/update")
def update_location(
    latitude: float,
    longitude: float,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "technician":
        raise HTTPException(status_code=403, detail="Only technicians")

    location = TechnicianLocation(
        technician_id=current_user.id,
        latitude=latitude,
        longitude=longitude,
        updated_at=datetime.utcnow()
    )

    db.add(location)
    db.commit()

    return {"message": "Location updated"}


@router.get("/tracking/{technician_id}")
def get_location(technician_id: int, db: Session = Depends(get_db)):
    return db.query(TechnicianLocation).filter(
        TechnicianLocation.technician_id == technician_id
    ).order_by(TechnicianLocation.updated_at.desc()).first()