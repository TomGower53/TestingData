# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session


# Write directly to the app
st.title(f":tractor: Machine Order")
st.write(
  """Check out these machines
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

# Get the current credentials
session = get_active_session()
