from loguru import logger

from nodes.database import VENDOR_DB


def service_summarizer_node(state: dict) -> dict:
    date = state['date']
    vendor_info = VENDOR_DB.get(date, {})
    services = vendor_info.get('services', [])
    summary = f"Services provided by {state['vendor_name']}: {', '.join(services)}"
    logger.info(f"Services summary: {summary}")
    return {"services_summary": summary}