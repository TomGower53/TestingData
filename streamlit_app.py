# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.image('https://www.clipartmax.com/middle/m2i8m2A0K9H7H7d3_avant-logo-avant-logo/', width="content")
st.title(f":tractor: Machine Order")

customer_name = st.text_input('Purchaser Name:')

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()

sales_member = session.table("TEST_DATABASE.PUBLIC.SALES_TEAM").select(col('Sales Team Name')).filter(col('Current_Employee')==1)
#st.dataframe(data=sales_member, use_container_width=True)
st.selectbox('Sales Representative:', sales_member, index=None)
