import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
import datetime
from loguru import logger

# Import node functions (to be implemented)
from nodes.vendor_selector_node import vendor_selector_node
from nodes.service_summarizer_node import service_summarizer_node
from nodes.payment_assessor_node import payment_assessor_node
from nodes.payment_sender_node import payment_sender_node

load_dotenv()


class PaymentState(TypedDict):
    date: str
    vendor_name: str
    services_summary: str
    payment_amount: float
    payment_details: Dict[str, any]


workflow = StateGraph(PaymentState)

# Add nodes
workflow.add_node("vendor_selector", vendor_selector_node)
workflow.add_node("service_summarizer", service_summarizer_node)
workflow.add_node("payment_assessor", payment_assessor_node)
workflow.add_node("payment_sender", payment_sender_node)

# Set up the workflow
workflow.set_entry_point("vendor_selector")
workflow.add_edge("vendor_selector", "service_summarizer")
workflow.add_edge("service_summarizer", "payment_assessor")
workflow.add_edge("payment_assessor", "payment_sender")
workflow.add_edge("payment_sender", END)

app = workflow.compile()


def run_workflow(date: str):
    for s in app.stream({"date": date}):
        logger.info(f"Step completed: {list(s.keys())[0]}")
        logger.info(f"Current state: {s}")

    return s


def process_payment(date: str):
    try:
        result = run_workflow(date)
        # Extract the last state from the workflow result
        last_state = list(result.values())[-1] if result else {}

        if isinstance(last_state, dict) and 'payment_details' in last_state:
            return {"payment_details": last_state['payment_details']}
        else:
            return {"error": "Payment processing did not complete as expected", "last_state": last_state}
    except Exception as e:
        logger.error(f"Error in process_payment: {str(e)}")
        return {"error": str(e)}
