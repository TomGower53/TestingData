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
            if vehicle_selection == "800":
                st.image('https://www.avanttecno.com/application/files/3415/6094/9554/Avant-860i.jpg', width=500, horizontal_alignment="center")
            
            st.dataframe(data=chosen_vehicle_data, use_container_width=True, hide_index=True)

            vehicle_cost = session.table("TEST_DATABASE.PUBLIC.VEHICLE_OPTIONS").filter(col('"Vehicle"')==vehicle_selection).select(col('"Cost"'))
            def vehicle_cost_pd():
                return vehicle_cost.to_pandas()
            vehicle_cost_table=vehicle_cost_pd()
            vehicle_cost_table1 = vehicle_cost_table.rename(columns={"Cost": "Add On Cost"})
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
                def tyre_cost_pd():
                    return tyre_cost.to_pandas()
                tyre_cost_table=tyre_cost_pd()
                #st.write(tyre_cost)

                st.subheader("""Booms for """+vehicle_selection)
                boom_list = session.table("TEST_DATABASE.PUBLIC.BOOM_FOR_VEHICLES").filter(col('"Vehicle"')==vehicle_selection).select(col('"Boom Type"'),col('"Cost"'),col('"Load Capacity (KG)"'),col('"Add On Cost"'))
                accessories_cols = ["Boom Type", "Cost", "Load Capacity (KG)"]
                #st.dataframe(data=boom_list, use_container_width=True, hide_index=True)

                accessories = st.multiselect ('Add the accessories you wish to include', boom_list, key="accessories")

                sorted_accessories = sorted(accessories, key=lambda x: x[10], reverse=True)
                accessories_string = ", ".join(sorted_accessories)
                
                st.dataframe(data=boom_list, use_container_width=True, hide_index=True, column_order=accessories_cols)

                #st.write(accessories_string)
                #st.dataframe(data=accessories, hide_index=True)
                
                st.subheader("""Order Summary for """+customer_name)
                
                if accessories:
                    accessories_cost = boom_list[boom_list["Boom Type"].isin(accessories)].select(col('"Add On Cost"'))
                    def accessories_cost_pd():
                        return accessories_cost.to_pandas()
                    accessories_cost_table=accessories_cost_pd()
                    #st.dataframe(data=accessories_cost, use_container_width=True, hide_index=True)

                    all_cost = pd.concat([vehicle_cost_table1, tyre_cost_table, accessories_cost_table])
                    #st.dataframe(all_cost)
                    all_cost_total = all_cost["Add On Cost"].sum()
                    #st.write(all_cost_total)

                    order_summary = """The """+vehicle_selection+""" with """+tyre_selection+""" tyres and """+accessories_string+""" accessories. Currently priced at £"""+str(all_cost_total)+"""."""
                    st.write(order_summary)
                    
                    my_insert_stmt = """ INSERT INTO TEST_DATABASE.PUBLIC.CUSTOMER_ORDERS("Customer", "Sales Representative", "Vehicle", "Tyres", "Accessories")
                        VALUES ('""" + customer_name + """','"""+sales_rep_string+ """','"""+vehicle_selection+ """','"""+tyre_selection+ """','"""+accessories_string+ """')"""

                    def insert_stm():
                            session.sql(my_insert_stmt).collect()
                        
                    confirm_order = st.button('Submit order', on_click=insert_stm)
                
                    if confirm_order:
                        st.success("Your order has been placed. Once this has been processed, an invoice will be sent over.", icon="✅")                           

                else:
                
                    all_cost1 = pd.concat([vehicle_cost_table1, tyre_cost_table])
                    all_cost_total1 = all_cost1["Add On Cost"].sum()
                    
                    order_summary1 = """The """+vehicle_selection+""" with """+tyre_selection+""" tyres and no further accessories. Currently priced at £"""+str(all_cost_total1)+"""."""
                    st.write(order_summary1)

                    my_insert_stmt1 = """ insert into test_database.public.customer_orders("Customer", "Sales Representative", "Vehicle", "Tyres")
                        values ('""" + customer_name + """','"""+sales_rep_string+ """','"""+vehicle_selection+ """','"""+tyre_selection+ """')"""

                    def insert_stm1():
                            session.sql(my_insert_stmt1).collect()
                
                    confirm_order1 = st.button('Submit order', on_click=insert_stm1)

                    if confirm_order1:
                        st.success("Your order has been placed. Once this has been processed, an invoice will be sent over.", icon="✅")
                    

    clear_name = st.button("Clear form", on_click=clear_all_names)

    if clear_name:
        st.error("Are you sure you'd like to clear the form?")
        if st.button("Confirm"):
            run_expensive_function()
