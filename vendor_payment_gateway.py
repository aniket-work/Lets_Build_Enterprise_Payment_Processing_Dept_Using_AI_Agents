from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from loguru import logger

app = FastAPI()


class PaymentDetails(BaseModel):
    vendor: str
    amount: float
    date: str
    services: str


@app.post("/process_payment")
async def process_payment(payment: PaymentDetails):
    logger.info(f"Received payment: {payment.dict()}")
    # In a real scenario, you would process the payment here
    return {"status": "Payment processed successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)