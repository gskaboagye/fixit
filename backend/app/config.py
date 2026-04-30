from dotenv import load_dotenv
import os

load_dotenv()

# ======================
# DATABASE
# ======================
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set!")


# ======================
# SECURITY
# ======================
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("❌ SECRET_KEY is not set!")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)


# ======================
# PAYSTACK
# ======================
PAYSTACK_SECRET = os.getenv("PAYSTACK_SECRET")
if not PAYSTACK_SECRET:
    print("⚠️ WARNING: PAYSTACK_SECRET not set (payments will fail)")