from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from database import collection
from datetime import datetime
from fraud_detection import check_duplicate, check_frequency
from logger import logger

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home():
    return {"message": "API is running"}
@app.get("/dashboard")
def dashboard(request: Request):
    data = list(collection.find())

    total = len(data)
    success = len([x for x in data if x["status"] == "success"])
    failed = len([x for x in data if x["status"] == "failed"])

    return templates.TemplateResponse("index.html", {
        "request": request,
        "transactions": data,
        "total": total,
        "success": success,
        "failed": failed
    })
class Transaction(BaseModel):
    transaction_id: str
    amount: float
    sender: str
    receiver: str

@app.post("/validate")
def validate(tx: Transaction):
    try:
        logger.info(f"Received transaction: {tx.transaction_id}")

        status = "success"
        reason = None
        flags = []

        # Basic validation
        if tx.amount <= 0:
            status = "failed"
            reason = "Invalid amount"

        elif tx.sender == tx.receiver:
            status = "failed"
            reason = "Same account"

        # Fraud checks
        if check_duplicate(tx.transaction_id):
            flags.append("Duplicate Transaction")

        if check_frequency(tx.sender):
            flags.append("Too many transactions in short time")

        if tx.amount > 100000:
            flags.append("High transaction")

        # Store in DB
        collection.insert_one({
            "transaction_id": tx.transaction_id,
            "amount": tx.amount,
            "sender": tx.sender,
            "receiver": tx.receiver,
            "status": status,
            "reason": reason,
            "flags": flags,
            "timestamp": datetime.now()
        })

        logger.info("Transaction processed")

        return {
            "status": status,
            "reason": reason,
            "flags": flags
        }

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {"status": "error"}

