# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd
#import time

# Write directly to the app
st.image('https://hydnum.com/wp-content/uploads/2020/11/avant-logo-new-png-1.png', width="content")
st.title(f":tractor: Sales Team App :tractor:")

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()

def clear_all_names():
    st.session_state["email"] = ""
    st.session_state["contact_number"] = ""
    st.session_state["company"] = ""
    st.session_state["address_1"] = ""
    st.session_state["address_2"] = ""
    st.session_state["town"] = ""
    st.session_state["county"] = ""
    st.session_state["postcode"] = ""


sales_member = session.table("TEST_DATABASE.PUBLIC.SALES_TEAM").select(col('Sales Team Name')).filter(col('Current_Employee')==1)
sales_rep_string = st.selectbox('Sales Representative:', sales_member, index=None, key="sales_rep")

sales_data = session.table("TEST_DATABASE.PUBLIC.MONTHLY_SALES").filter(col('"LatestMonth"')==1)

missing_customer_details = session.table("TEST_DATABASE.PUBLIC.ORDER_SUMMARY").filter(col('"ValidCustomer"')==0).select(col('"Customer"'),col('"Order Summary"'),col('"Full Cost"'))
def load_table_cd():
    return missing_customer_details.to_pandas()
cd_rows=load_table_cd()

sm_missing_customer_details = session.table("TEST_DATABASE.PUBLIC.ORDER_SUMMARY").filter(col('"ValidCustomer"')==0).filter(col('"Sales Representative"')==sales_rep_string).select(col('"Customer"'),col('"Order Summary"'),col('"Full Cost"'))    
def load_table_sm_cd():
    return sm_missing_customer_details.to_pandas()
sm_cd_rows=load_table_sm_cd()

pending_orders = session.table("TEST_DATABASE.PUBLIC.ORDER_SUMMARY").filter(col('"Order Completed"')==0).filter(col('"ValidCustomer"')==1).select(col('"Sales Representative"'),col('"Order Status"'),col('"Order Summary"'),col('"Full Cost"'))
def load_table_po():
    return pending_orders.to_pandas()
po_rows=load_table_po()

sm_pending_orders = session.table("TEST_DATABASE.PUBLIC.ORDER_SUMMARY").filter(col('"Order Completed"')==0).filter(col('"ValidCustomer"')==1).filter(col('"Sales Representative"')==sales_rep_string).select(col('"Customer"'),col('"Order Status"'),col('"Order Summary"'),col('"Full Cost"'))
def load_table_sm_po():
    return sm_pending_orders.to_pandas()
sm_po_rows=load_table_sm_po()

if sales_rep_string:
    if not sm_cd_rows.empty:
        st.subheader('Missing Customer Details & Orders')
        st.dataframe(data=sm_missing_customer_details, width="stretch", hide_index=True)

        with st.form("my_form"):
            st.write("Customer Details Form")
            customer_name = st.selectbox('Missing Customer:', sm_missing_customer_details, index=None)
            email = st.text_input('Email:', key="email")
            contact_number = st.text_input('Contact Number:', max_chars=15, key="contact_number")
            company = st.text_input('Company:', key="company")
            address_1 = st.text_input('Address Line 1:', key="address_1")
            address_2 = st.text_input('Address Line 2:', key="address_2")
            town = st.text_input('Town/City:', key="town")
            county = st.text_input('County:', key="county")
            country = st.text_input('Country:', value="United Kingdom")
            postcode = st.text_input('Post Code:', max_chars=8, key="postcode")
            Marketing = st.checkbox("Marketing Opt In", value=True)

            submitted = st.form_submit_button("Submit")

        if submitted:
        
            if Marketing:
                Market = '1'
            else:
                Market = '0'
        
            if not customer_name or not email or not contact_number or not postcode:
                st.warning("Please ensure all mandatory fields are populated")
                st.stop()
            else:
                customer_dets = """ INSERT INTO TEST_DATABASE.PUBLIC.CUSTOMERS("Customer Name", "Email", "Contact Number", "Company", "Address Line 1", "Address Line 2", "Town/City", "County", "Country", "Post Code", "Marketing Opt In")
                    VALUES ('""" + customer_name + """','"""+email+ """','"""+contact_number+ """','"""+company+ """','"""+address_1+ """','"""+address_2+ """','"""+town+ """','"""+county+ """','"""+country+ """','"""+postcode+ """','"""+Market+ """')"""

                st.success("Form submitted")
                session.sql(customer_dets).collect()

                st.button("Clear form", on_click=clear_all_names)

    st.subheader('Pending Customer Orders')
    if not sm_po_rows.empty:
        st.dataframe(data=sm_pending_orders, width="stretch", hide_index=True)
    else:
        st.write("""There are no pending orders sold by """+sales_rep_string+""".""")
        
else:
    if not cd_rows.empty:
        st.subheader('Missing Customer Details & Orders')
        st.dataframe(missing_customer_details, width="stretch", hide_index=True)
    
        with st.form("my_form"):
            st.write("Customer Details Form")
            customer_name = st.selectbox('Missing Customer:', missing_customer_details, index=None)
            email = st.text_input('Email:', key="email")
            contact_number = st.text_input('Contact Number:', max_chars=15, key="contact_number")
            company = st.text_input('Company:', key="company")
            address_1 = st.text_input('Address Line 1:', key="address_1")
            address_2 = st.text_input('Address Line 2:', key="address_2")
            town = st.text_input('Town/City:', key="town")
            county = st.text_input('County:', key="county")
            country = st.text_input('Country:', value="United Kingdom")
            postcode = st.text_input('Post Code:', max_chars=8, key="postcode")
            Marketing = st.checkbox("Marketing Opt In", value=True)

            submitted = st.form_submit_button("Submit")

        
        if submitted:
        
            if Marketing:
                Market = '1'
            else:
                Market = '0'
        
            if not customer_name or not email or not contact_number or not postcode:
                st.warning("Please ensure all mandatory fields are populated")
                st.stop()
            else:
                customer_dets = """ INSERT INTO TEST_DATABASE.PUBLIC.CUSTOMERS("Customer Name", "Email", "Contact Number", "Company", "Address Line 1", "Address Line 2", "Town/City", "County", "Country", "Post Code", "Marketing Opt In")
                    VALUES ('""" + customer_name + """','"""+email+ """','"""+contact_number+ """','"""+company+ """','"""+address_1+ """','"""+address_2+ """','"""+town+ """','"""+county+ """','"""+country+ """','"""+postcode+ """','"""+Market+ """')"""

                st.success("Form submitted")
                session.sql(customer_dets).collect()

                st.button("Clear form", on_click=clear_all_names)

    st.subheader('Pending Customer Orders')
    if not po_rows.empty:
        st.dataframe(data=pending_orders, width="stretch", hide_index=True)
    else:
        st.write("There are no pending orders.")

st.subheader('Latest Month Sales')
st.write("Sales By Team Member")
st.bar_chart(data=sales_data, x="Sales Representative", y="Sales Volumes")
st.write("Sales Cost By Team Member")
st.bar_chart(data=sales_data, x="Sales Representative", y="Sales Cost")
