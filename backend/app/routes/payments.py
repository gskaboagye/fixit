import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ServiceRequest
from app.config import PAYSTACK_SECRET

router = APIRouter()

@router.post("/verify-payment")
def verify_payment(data: dict, db: Session = Depends(get_db)):

    reference = data["reference"]
    request_id = data["request_id"]

    url = f"https://api.paystack.co/transaction/verify/{reference}"

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET}"
    }

    res = requests.get(url, headers=headers)
    response = res.json()

    if response["data"]["status"] == "success":

        request_item = db.query(ServiceRequest).filter(
            ServiceRequest.id == request_id
        ).first()

        if not request_item:
            return {"error": "Request not found"}

        request_item.status = "paid"

        db.commit()
        db.refresh(request_item)

        return {"message": "✅ Payment verified"}

    return {"error": "Payment failed"}