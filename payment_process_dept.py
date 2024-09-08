import streamlit as st
from datetime import datetime
from payment_processing_workflow import process_payment

st.title("Payment Processing Department")

date = st.date_input("Select payment date", datetime.now())

if st.button("Process Payment"):
    with st.spinner("Processing payment..."):
        result = process_payment(date.strftime("%Y-%m-%d"))

    if isinstance(result, dict):
        if "error" in result:
            st.error(f"Error processing payment: {result['error']}")
        elif "payment_details" in result:
            st.success("Payment processed successfully!")
            st.json(result["payment_details"])
        else:
            st.warning("Payment processed, but no details were returned.")
            st.json(result)
    else:
        st.error(f"Unexpected result type: {type(result)}. Please check the process_payment function.")

st.sidebar.header("Logs")
# In a real application, you would stream logs from a file or database
st.sidebar.text_area("Log Output", value="Log messages will appear here...", height=300)