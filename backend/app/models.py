from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


# ======================
# USERS
# ======================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    password = Column(String, nullable=False)

    role = Column(String, default="user")

    created_at = Column(DateTime, default=datetime.utcnow)

    requests = relationship("ServiceRequest", back_populates="user")
    messages = relationship("ChatMessage", back_populates="sender")


# ======================
# TECHNICIANS
# ======================
class Technician(Base):
    __tablename__ = "technicians"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    location = Column(String)

    is_available = Column(Boolean, default=True)

    # 🔥 PAYMENT SPLIT
    subaccount_code = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    requests = relationship("ServiceRequest", back_populates="technician")
    reviews = relationship("Review", back_populates="technician")


# ======================
# SERVICE REQUEST
# ======================
class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    technician_id = Column(Integer, ForeignKey("technicians.id"))

    service_type = Column(String, nullable=False)
    description = Column(Text)
    location = Column(String)

    status = Column(String, default="pending")

    # 🔥 PAYMENT INFO
    amount = Column(Float, default=50.0)
    payment_reference = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="requests")
    technician = relationship("Technician", back_populates="requests")

    messages = relationship("ChatMessage", back_populates="request")
    reviews = relationship("Review", back_populates="request")


# ======================
# CHAT SYSTEM 💬
# ======================
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(Integer, ForeignKey("service_requests.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))

    message = Column(Text, nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow)

    request = relationship("ServiceRequest", back_populates="messages")
    sender = relationship("User", back_populates="messages")


# ======================
# REVIEWS ⭐
# ======================
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(Integer, ForeignKey("service_requests.id"))
    technician_id = Column(Integer, ForeignKey("technicians.id"))

    rating = Column(Integer)
    comment = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    technician = relationship("Technician", back_populates="reviews")
    request = relationship("ServiceRequest", back_populates="reviews")


# ======================
# LIVE TRACKING 📍
# ======================
class TechnicianLocation(Base):
    __tablename__ = "technician_locations"

    id = Column(Integer, primary_key=True, index=True)

    technician_id = Column(Integer, ForeignKey("technicians.id"))

    latitude = Column(Float)
    longitude = Column(Float)

    updated_at = Column(DateTime, default=datetime.utcnow)