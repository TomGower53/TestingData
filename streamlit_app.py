# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.image('https://hydnum.com/wp-content/uploads/2020/11/avant-logo-new-png-1.png', width="content")
st.title(f":tractor: Machine Order")

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()

def clear_text():
    st.session_state["input"] = ""
    
customer_name = st.text_input('Purchaser Name:')
name_placeholder = st.empty()
    
if st.button('Submit order', on_click=clear_text):
    customer_name.empty()

st.stop()

customer_name = st.text_input('Purchaser Name:')

if customer_name:

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

            st.subheader("""Tyres for """+vehicle_selection)
            tyre_list = session.table("TEST_DATABASE.PUBLIC.TYRES_FOR_VEHICLES").filter(col('"Vehicle"')==vehicle_selection).select(col('"Tyres"'),col('"Cost"'),col('"Size"'),col('"Warranty"'),col('"Economy"'),col('"Grip"'))
            st.dataframe(data=tyre_list, use_container_width=True, hide_index=True)

            tyre_selection = st.selectbox('Which tyres are you interested in?', tyre_list, index=0)

            st.subheader("""Booms for """+vehicle_selection)
            boom_list = session.table("TEST_DATABASE.PUBLIC.BOOM_FOR_VEHICLES").filter(col('"Vehicle"')==vehicle_selection).select(col('"Boom Type"'),col('"Cost"'),col('"Load Capacity (KG)"'))
            st.dataframe(data=boom_list, use_container_width=True, hide_index=True)

            accessories = st.multiselect ('Add the accessories you wish to include', boom_list)

            accessories_string = ", ".join(accessories)

            st.write(accessories_string)
            #st.dataframe(data=accessories, use_container_width=True, hide_index=True)
            
            if accessories:
                order_summary = """The order for """+customer_name+""" by """+sales_rep_string+""" is as follows. The """+vehicle_selection+""" with """+tyre_selection+""" tyres and """+accessories_string+""" accessories."""
                st.write(order_summary)
                confirm_order = st.button('Submit order')

                if confirm_order:
                    st.success("""Your order is currently pending. """+order_summary+""" If this is correct, confirm below and your order will be placed.""", icon="✅")
                    
                    place_order = st.button('Confirm order')

                    if place_order:
                        st.write("Thank you for the order")
                        customer_name.empty()
                        sales_rep_string.empty()
                        vehicle_selection.empty()
                        accessories.empty()
            else:
                
                order_summary1 = """The order for """+customer_name+""" by """+sales_rep_string+""" is as follows. The """+vehicle_selection+""" with """+tyre_selection+""" tyres and no further accessories."""
                st.write(order_summary1)

                confirm_order1 = st.button('Submit order')

                if confirm_order1:
                    st.success("""Your order is currently pending. """+order_summary1+""" If this is correct, confirm below and your order will be placed.""", icon="✅")
                    
                    place_order1 = st.button('Confirm order')

                    if place_order1:
                        st.write("Thank you for the order")
                        customer_name.empty()
                        sales_rep_string.empty()
                        vehicle_selection.empty()
