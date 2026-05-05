from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app import models, schemas
from app.security import hash_password, verify_password


# ======================
# USER
# ======================
def create_user(db: Session, user: schemas.UserCreate):
    try:
        hashed_pw = hash_password(user.password)

        db_user = models.User(
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            password=hashed_pw,  # ⚠️ Ensure your model uses "password"
            role=user.role
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    except Exception as e:
        db.rollback()
        print("🔥 CREATE USER ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


def authenticate_user(db: Session, email: str, password: str):
    try:
        user = db.query(models.User).filter(models.User.email == email).first()

        if not user or not verify_password(password, user.password):
            return None

        return user

    except Exception as e:
        print("🔥 AUTH ERROR:", str(e))
        return None


# ======================
# TECHNICIAN
# ======================
def create_technician(db: Session, tech: schemas.TechnicianCreate):
    try:
        technician = models.Technician(
            full_name=tech.full_name,
            phone=tech.phone,
            service_type=tech.service_type,
            location=tech.location,
            is_available=True
        )

        db.add(technician)
        db.commit()
        db.refresh(technician)

        return technician

    except Exception as e:
        db.rollback()
        print("🔥 TECHNICIAN ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to create technician"
        )


# ======================
# SERVICE REQUEST
# ======================
def create_request(db: Session, request: schemas.ServiceRequestCreate, user_id: int):
    try:
        new_request = models.ServiceRequest(
            service_type=request.service_type,
            description=request.description,
            location=request.location,
            user_id=user_id,
            status="pending",
            amount=50.0
        )

        db.add(new_request)
        db.commit()
        db.refresh(new_request)

        return new_request

    except Exception as e:
        db.rollback()
        print("🔥 REQUEST ERROR:", str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to create request"
        )


def get_user_requests(db: Session, user_id: int):
    return db.query(models.ServiceRequest).filter(
        models.ServiceRequest.user_id == user_id
    ).all()


# ======================
# MATCHING
# ======================
def match_technicians(db: Session, request_id: int):
    request = db.query(models.ServiceRequest).filter(
        models.ServiceRequest.id == request_id
    ).first()

    if not request:
        return None

    return db.query(models.Technician).filter(
        models.Technician.service_type == request.service_type,
        models.Technician.location == request.location,
        models.Technician.is_available == True
    ).all()


# ======================
# ASSIGNMENT
# ======================
def assign_technician(db: Session, request_id: int, technician_id: int):
    try:
        request = db.query(models.ServiceRequest).filter(
            models.ServiceRequest.id == request_id
        ).first()

        if not request:
            raise HTTPException(status_code=404, detail="Request not found")

        if request.technician_id:
            raise HTTPException(status_code=400, detail="Already assigned")

        technician = db.query(models.Technician).filter(
            models.Technician.id == technician_id
        ).first()

        if not technician or not technician.is_available:
            raise HTTPException(status_code=400, detail="Technician not available")

        request.technician_id = technician.id
        request.status = "assigned"
        technician.is_available = False

        db.commit()
        db.refresh(request)

        return request

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        print("🔥 ASSIGN ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Assignment failed")


# ======================
# STATUS UPDATE
# ======================
def update_request_status(db: Session, request_id: int, new_status: str):
    try:
        request = db.query(models.ServiceRequest).filter(
            models.ServiceRequest.id == request_id
        ).first()

        if not request:
            raise HTTPException(status_code=404, detail="Request not found")

        valid_statuses = ["pending", "assigned", "in_progress", "completed", "paid"]

        if new_status not in valid_statuses:
            raise HTTPException(status_code=400, detail="Invalid status")

        request.status = new_status

        # Free technician after completion
        if new_status in ["completed", "paid"] and request.technician:
            request.technician.is_available = True

        db.commit()
        db.refresh(request)

        return request

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        print("🔥 STATUS ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Status update failed")


# ======================
# TECHNICIAN DASHBOARD
# ======================
def get_technician_jobs(db: Session, technician_id: int):
    return db.query(models.ServiceRequest).filter(
        models.ServiceRequest.technician_id == technician_id
    ).all()


# ======================
# ACCEPT JOB
# ======================
def accept_job(db: Session, request_id: int, technician_id: int):
    try:
        request = db.query(models.ServiceRequest).filter(
            models.ServiceRequest.id == request_id
        ).first()

        if not request or request.technician_id != technician_id:
            raise HTTPException(status_code=400, detail="Invalid request")

        request.status = "in_progress"

        db.commit()
        db.refresh(request)

        return request

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        print("🔥 ACCEPT ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Failed to accept job")


# ======================
# REJECT JOB
# ======================
def reject_job(db: Session, request_id: int, technician_id: int):
    try:
        request = db.query(models.ServiceRequest).filter(
            models.ServiceRequest.id == request_id
        ).first()

        if not request or request.technician_id != technician_id:
            raise HTTPException(status_code=400, detail="Invalid request")

        request.technician_id = None
        request.status = "pending"

        technician = db.query(models.Technician).filter(
            models.Technician.id == technician_id
        ).first()

        if technician:
            technician.is_available = True

        db.commit()
        db.refresh(request)

        return request

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        print("🔥 REJECT ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Failed to reject job")