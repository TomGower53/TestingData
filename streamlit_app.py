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

vehicle_data = session.table("TEST_DATABASE.PUBLIC.VEHICLES")
vehicle_list = session.table("TEST_DATABASE.PUBLIC.VEHICLE_OPTIONS").select(col('"Vehicle"'))


if sales_rep_string:

    st.subheader('Vehicles')
    st.dataframe(data=vehicle_data, use_container_width=True, hide_index=True)

    vehicle_selection = st.selectbox('Which vehicle are you interested in?', vehicle_list, index=None)

    if vehicle_selection:

        vehicle_data = session.table("TEST_DATABASE.PUBLIC.TYRES_FOR_VEHICLES").filter(col('"Vehicle"')==vehicle"Economy"_selection).select(col('"Tyres"'),col('"Cost"'),col('"Size (In)"'),col('"Warranty"'),col('"Economy"'),col('"Grip"'))
        st.dataframe(data=vehicle_data, use_container_width=True, hide_index=True)
