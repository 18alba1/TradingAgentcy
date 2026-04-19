'''
take user input (stock ticker)
trigger pipeline execution
display results
show agent outputs in Streamlit
'''

import streamlit as st
from src.data.stock_data import get_stock_data
from src.agents.technical_agent import technical_agent

st.title("Trading Agent System")

st.write("System is running 🚀")

data = get_stock_data("AAPL")
st.write(technical_agent(data))