
import json
from datetime import datetime
import requests
from loguru import logger


def payment_sender_node(state: dict) -> dict:
    payment_details = {
        "vendor": state['vendor_name'],
        "amount": state['payment_amount'],
        "date": state['date'],
        "services": state['services_summary']
    }

    # Send payment details to FastAPI endpoint
    try:
        response = requests.post("http://localhost:8000/process_payment", json=payment_details)
        response.raise_for_status()
        logger.info(f"Payment sent successfully: {payment_details}")
    except requests.RequestException as e:
        logger.error(f"Failed to send payment: {e}")
        return {"error": str(e)}

    return {"payment_details": payment_details}