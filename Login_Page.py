# Importing necessary Python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

# Get the current Snowflake session
session = get_active_session()


# Function to validate the user credentials
def validate_credentials(user, pwd):

    query = f"""Select True from STREAMLIT.APPS.USER_DETAIL where upper(u_name) = upper('{user}') and password = '{pwd}';"""
    result=session.sql(query).collect()
    if result:
        return True
        
        #st.success("User Validated")
    else:
        #st.error("Invalid User")
        return False

# Function to display the login page
def login_page():
    # Set the title of the Streamlit app
    st.title(':blue[LOGIN PAGE]')
    
    # Create a username input box with placeholder text "user"
    username = st.text_input("Username", placeholder="user", help='Provide your user name').strip()
    
    # Create a password input box
    password = st.text_input("Password", type="password", help='Provide your password')
    
    # Submit button
    # When the button is clicked, the entered username and password are stored in the database
    if st.button(":red[Submit]"):
        if username == "":
            st.warning("Username cannot be empty!")
        elif password.strip() == "":
            st.warning("Password cannot be empty!")
        else: 
             # Validate username and password
               if validate_credentials(username, password):
                st.success("Login successful!")
               else:
                st.error("Incorrect username or password. Please try again.")


login_page()