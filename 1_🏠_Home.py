import pickle
from pathlib import Path
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth

page_title = "Health Pilot"
page_icon = "⚕️"
layout = "centered"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

# Move the logo image to the top of the sidebar
with st.sidebar:
    st.image("images/Logoo.png")

# User Authentication
# names=["Ayesha Siddiqua", "Asma Khanam"]
# usernames=["ayesha","asma"]
# passwords=["XXX","XXX"]

# file_path = Path(__file__).parent / "hashed_pw.pkl"
# with file_path.open("rb") as file:
#     hashed_passwords = pickle.load(file)

# authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
#     "health_dashboard", "abcdef",30)

# name, authentication_status, username = authenticator.login("Login", "main")

# if authentication_status == False:
#     st.error("Username/password is incorrect")

# if authentication_status == None:
#     st.warning("Please enter your username and password")

# if authentication_status:
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.title(page_title)


