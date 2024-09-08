from loguru import logger

from nodes.database import VENDOR_DB
from nodes.llm_service import llm_service


def service_summarizer_node(state: dict) -> dict:
    prompt_template = """
    system
    You are an expert at summarizing services provided by vendors. Given a list of services, provide a detailed summary of what these services entail and their potential impact on the business. Return your response as JSON with a single key called 'services_summary'.
    user
    VENDOR: {vendor_name}
    SERVICES: {services}
    assistant
    """

    services = VENDOR_DB.get(state['date'], {}).get('services', [])
    response = llm_service.generate_response(prompt_template, {
        "vendor_name": state['vendor_name'],
        "services": ", ".join(services)
    })

    logger.info(f"Services summary generated: {response['services_summary']}")
    return response
