
import json
from datetime import datetime
import requests
from loguru import logger

from nodes.llm_service import llm_service


def payment_sender_node(state: dict) -> dict:
    prompt_template = """
    system
    You are a financial reporting expert responsible for generating detailed payment reports. Given the payment details, create a comprehensive report explaining the payment process, amount, and services covered. Return your response as JSON with a single key called 'payment_report'.
    user
    VENDOR: {vendor_name}
    AMOUNT: ${payment_amount}
    SERVICES SUMMARY: {services_summary}
    ASSESSMENT EXPLANATION: {assessment_explanation}
    assistant
    """

    response = llm_service.generate_response(prompt_template, {
        "vendor_name": state['vendor_name'],
        "payment_amount": state['payment_amount'],
        "services_summary": state['services_summary'],
        "assessment_explanation": state['assessment_explanation']
    })

    payment_details = {
        "vendor": state['vendor_name'],
        "amount": state['payment_amount'],
        "date": state['date'],
        "services_summary": state['services_summary'],
        "assessment_explanation": state['assessment_explanation'],
        "payment_report": response['payment_report']
    }

    # Send payment details to FastAPI endpoint
    try:
        api_response = requests.post("http://localhost:8000/process_payment", json=payment_details)
        api_response.raise_for_status()
        logger.info(f"Payment sent successfully: {payment_details}")
    except requests.RequestException as e:
        logger.error(f"Failed to send payment: {e}")
        return {"error": str(e)}

    return {"payment_details": payment_details}
