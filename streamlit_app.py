# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd
#import time

# Write directly to the app
st.image('https://hydnum.com/wp-content/uploads/2020/11/avant-logo-new-png-1.png', width="content")
st.title(f":tractor: Machine Order")

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()

def clear_all_names():
    st.session_state["name"] = ""
    st.session_state["sales_rep"] = ""
    st.session_state["vehicle"] = ""
    st.session_state["accessories"] = ""
    
customer_name = st.text_input('Purchaser Name:', key="name")  

if customer_name:

    sales_member = session.table("TEST_DATABASE.PUBLIC.SALES_TEAM").select(col('Sales Team Name')).filter(col('Current_Employee')==1)
    #st.dataframe(data=sales_member, use_container_width=True)
    sales_rep_string = st.selectbox('Sales Representative:', sales_member, index=None, key="sales_rep")

    vehicle_data = session.table("TEST_DATABASE.PUBLIC.VEHICLES")
    vehicle_list = session.table("TEST_DATABASE.PUBLIC.VEHICLE_OPTIONS").select(col('"Vehicle"'))

    if sales_rep_string:

        st.subheader('Vehicles')
        vehicle_selection = st.selectbox('Which vehicle are you interested in?', vehicle_list, index=None, key="vehicle")
        
        if not vehicle_selection:
            st.dataframe(data=vehicle_data, use_container_width=True, hide_index=True)

        if vehicle_selection:
            
            chosen_vehicle_data = session.table("TEST_DATABASE.PUBLIC.VEHICLES").filter(col('"Vehicle"')==vehicle_selection).select(col('"Cost"'),col('"Lift Capacity (KG)"'),col('"Lift Height (m)"'),col('"Engine Power (hp)"'),col('"Maximum Speed (km/h)"'))
            st.dataframe(data=chosen_vehicle_data, use_container_width=True, hide_index=True)

            vehicle_cost = session.table("TEST_DATABASE.PUBLIC.VEHICLE_OPTIONS").filter(col('"Vehicle"')==vehicle_selection).select(col('"Cost"'))
            #st.dataframe(data=vehicle_cost, use_container_width=True, hide_index=True)
            
            st.subheader("""Tyres for """+vehicle_selection)
            tyre_list = session.table("TEST_DATABASE.PUBLIC.TYRES_FOR_VEHICLES").filter(col('"Vehicle"')==vehicle_selection).select(col('"Tyres"'),col('"Cost"'),col('"Size"'),col('"Warranty"'),col('"Economy"'),col('"Grip"'))

            tyre_selection = st.selectbox('Which tyres are you interested in?', tyre_list, index=None, key="tyres")
            
            if not tyre_selection:
                st.dataframe(data=tyre_list, use_container_width=True, hide_index=True)

            if tyre_selection:
                selected_tyres = session.table("TEST_DATABASE.PUBLIC.TYRES_FOR_VEHICLES").filter(col('"Vehicle"')==vehicle_selection).filter(col('"Tyres"')==tyre_selection).select(col('"Cost"'),col('"Size"'),col('"Warranty"'),col('"Economy"'),col('"Grip"'))
                st.dataframe(data=selected_tyres, use_container_width=True, hide_index=True)

                tyre_cost = session.table("TEST_DATABASE.PUBLIC.VEHICLE_ITEM_MAPPING").filter(col('"Vehicle"')==vehicle_selection).filter(col('"Part Name"')==tyre_selection).select(col('"Add On Cost"'))
                #st.write(tyre_cost)

                st.subheader("""Booms for """+vehicle_selection)
                boom_list = session.table("TEST_DATABASE.PUBLIC.BOOM_FOR_VEHICLES").filter(col('"Vehicle"')==vehicle_selection).select(col('"Boom Type"'),col('"Cost"'),col('"Load Capacity (KG)"'),col('"Add On Cost"'))
                accessories_cols = ["Boom Type", "Cost", "Load Capacity (KG)"]
                #st.dataframe(data=boom_list, use_container_width=True, hide_index=True)
                st.dataframe(data=boom_list, use_container_width=True, hide_index=True, column_order=accessories_cols)

                accessories = st.multiselect ('Add the accessories you wish to include', boom_list, key="accessories")

                accessories_string = ", ".join(accessories)

                #st.write(accessories_string)
                #st.dataframe(data=accessories, hide_index=True)
            
                if accessories:
                    accessories_cost = boom_list[boom_list["Boom Type"].isin(accessories)].select(col('"Add On Cost"'))
                    #st.dataframe(data=accessories_cost, use_container_width=True, hide_index=True)

                    order_summary = """The order for """+customer_name+""" by """+sales_rep_string+""" is as follows. The """+vehicle_selection+""" with """+tyre_selection+""" tyres and """+accessories_string+""" accessories."""
                    st.write(order_summary)

                    confirm_order = st.button('Submit order')
                
                    if confirm_order:
                        st.success("""Your order is currently pending. """+order_summary+""" If this is correct, confirm below and your order will be placed.""", icon="✅")

                        place_order = st.button('Confirm order')


                else:
                
                    order_summary1 = """The order for """+customer_name+""" by """+sales_rep_string+""" is as follows. The """+vehicle_selection+""" with """+tyre_selection+""" tyres and no further accessories."""
                    st.write(order_summary1)
                
                    confirm_order1 = st.button('Submit order')

                    if confirm_order1:
                        st.success("""Your order is currently pending. """+order_summary1+""" If this is correct, confirm below and your order will be placed.""", icon="✅")
                    
                        place_order1 = st.button('Confirm order')


    clear_name = st.button("Clear form", on_click=clear_all_names)

    if clear_name:
        st.error("Are you sure you'd like to clear the form?")
        if st.button("Confirm"):
            run_expensive_function()
