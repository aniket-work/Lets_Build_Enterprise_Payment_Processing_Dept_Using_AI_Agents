import json
from datetime import datetime
import requests
from loguru import logger

from nodes.llm_service import llm_service


def payment_assessor_node(state: dict) -> dict:
    prompt_template = """
    system
    You are an expert financial analyst responsible for assessing payment amounts for vendor services. Given a summary of services, determine an appropriate payment amount and provide a detailed explanation of your assessment. Return your response as JSON with keys 'payment_amount' (float) and 'assessment_explanation' (string).
    user
    VENDOR: {vendor_name}
    SERVICES SUMMARY: {services_summary}
    assistant
    """

    response = llm_service.generate_response(prompt_template, {
        "vendor_name": state['vendor_name'],
        "services_summary": state['services_summary']
    })

    logger.info(
        f"Payment assessment: Amount: ${response['payment_amount']}, Explanation: {response['assessment_explanation']}")
    return response
