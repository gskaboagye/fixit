from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ======================
# USER SCHEMAS
# ======================
class UserCreate(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str
    role: Optional[str] = None   # backend will set default


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    role: Optional[str] = "user"
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


# ======================
# TECHNICIAN SCHEMAS
# ======================
class TechnicianCreate(BaseModel):
    full_name: str
    phone: str
    service_type: str
    location: str


class TechnicianResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    service_type: str
    location: str
    is_available: bool

    class Config:
        from_attributes = True


# ======================
# SERVICE REQUEST SCHEMAS
# ======================
class ServiceRequestCreate(BaseModel):
    service_type: str
    description: str
    location: str


class ServiceRequestResponse(BaseModel):
    id: int
    service_type: str
    description: str
    location: str
    status: str

    user_id: Optional[int] = None
    technician_id: Optional[int] = None

    # 💳 PAYMENT
    amount: Optional[float] = 50.0
    payment_reference: Optional[str] = None

    created_at: datetime

    class Config:
        from_attributes = True


# ======================
# STATUS UPDATE
# ======================
class UpdateStatus(BaseModel):
    status: str


# ======================
# CHAT 💬
# ======================
class ChatCreate(BaseModel):
    request_id: int
    message: str


class ChatResponse(BaseModel):
    id: int
    request_id: int
    sender_id: int
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True


# ======================
# REVIEWS ⭐
# ======================
class ReviewCreate(BaseModel):
    request_id: int
    technician_id: int
    rating: int
    comment: str


class ReviewResponse(BaseModel):
    id: int
    request_id: int
    technician_id: int
    rating: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True


# ======================
# TRACKING 📍
# ======================
class LocationUpdate(BaseModel):
    latitude: float
    longitude: float


class LocationResponse(BaseModel):
    technician_id: int
    latitude: float
    longitude: float
    updated_at: datetime

    class Config:
        from_attributes = True