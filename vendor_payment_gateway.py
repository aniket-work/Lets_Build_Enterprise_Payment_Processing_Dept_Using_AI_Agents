from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from loguru import logger

app = FastAPI()


class PaymentDetails(BaseModel):
    vendor: str
    amount: float
    date: str
    services_summary: str
    assessment_explanation: str
    payment_report: str


@app.post("/process_payment")
async def process_payment(payment: Dict[str, Any]):
    logger.info(f"Received payment: {payment}")
    # In a real scenario, you would process the payment here
    return {"status": "Payment processed successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)