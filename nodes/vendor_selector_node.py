from loguru import logger

from nodes.database import VENDOR_DB


def vendor_selector_node(state: dict) -> dict:
    date = state['date']
    vendor_info = VENDOR_DB.get(date, {})
    vendor_name = vendor_info.get('vendor_name', 'Not found')
    logger.info(f"Selected vendor for {date}: {vendor_name}")
    return {"vendor_name": vendor_name}