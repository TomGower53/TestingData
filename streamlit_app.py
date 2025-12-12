# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.image('https://hydnum.com/wp-content/uploads/2020/11/avant-logo-new-png-1.png', width="content")
st.title(f":tractor: Machine Order")

customer_name = st.text_input('Purchaser Name:')

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()


sales_member = session.table("TEST_DATABASE.PUBLIC.SALES_TEAM").select(col('Sales Team Name')).filter(col('Current_Employee')==1)
#st.dataframe(data=sales_member, use_container_width=True)
sales_rep_string = st.selectbox('Sales Representative:', sales_member, index=None)

vehicle_list = session.table("TEST_DATABASE.PUBLIC.VEHICLE_OPTIONS").select(col('"Vehicle"'),col('"Lift Capacity (KG)"'),col('"Engine Power (hp)"'),col('"Lift Height (m)"'),col('"Maximum Speed (km/h)"'),col('"Cost"'))


if sales_rep_string:

    st.subheader('Vehicles')
    st.dataframe(data=vehicle_list, use_container_width=True)
