# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f":tractor: Machine Order")
st.write(
  """Check out these machines
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()
