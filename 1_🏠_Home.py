import json
import streamlit as st
from streamlit_option_menu import option_menu

page_title = "Health Pilot "
page_icon = "⚕️"
layout = "centered"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

with st.sidebar:
    st.image("images/Logoo.png")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1554120013-4ba50c1a1788?q=80&w=1770&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .shadow-text {
              text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.title('🩺 Welcome to :blue[Health Pilot]')

box_style = """
    background-color: #f0f0f0;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
"""
st.markdown(
    f"""
    <br>
    <div style="{box_style}">
        <h4 style="shadow-text;">Empowering Your Health Journey – Navigate, Analyze, Thrive!</h4>
        <p>This platform is designed to help predict and analyze your health reports. Our platform leverages state-of-the-art machine learning models to provide swift and accurate predictions based on the data you input. Whether you're assessing your risk factors, monitoring your health journey, or seeking preventive measures, our user-friendly interface empowers you with valuable insights. Your well-being is our priority, and we are here to guide you through your health analysis journey. Analyze, understand, and thrive with our Health Analyzer!</p>
    </div>
    <br>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    f"""
    <div style="{box_style}">
        <h4 style='color: #0066cc;'>How it Works!</h4>
        <ul>
            <li>Choose a specific Analyser from the sidebar.</li>
            <li>Enter the relevant data for prediction or analysis.</li>
            <li>Get instant results based on our trained machine learning models!</li>
        </ul>
    </div>
    <br>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style="{box_style}">
        <h4 style='color: #0066cc;'>Features</h4>
        <ul>
            <li>Safely store and manage your previous health reports, creating a comprehensive archive for easy reference and tracking.</li>
            <li>Experience a seamless and user-friendly interface designed to simplify your health journey.</li>
            <li>Also provides Guidelines for effective diabetes control.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)
st.balloons()

def create_footer():
    footer= """
            background-color: #f0f0f0;
            padding: 20px;
            text-align: center;
            bottom: 0;
            width: 100%;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        """

    button="""
            background-color: #e78b2c; 
            color: #fff;
            padding: 5px 5px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        """

    st.markdown(
        f"""
        <br>
        <br>
        <div style="{footer}">
            <a style="{button}" href="https://github.com/Ayesha-Siddiqua88" target="_blank">GitHub</a>
            <br>
            <br>
            <p>Privacy | Health | Terms</p>
            <p><i>Made with 💙 by AA</i></p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Use the footer in your Streamlit app
create_footer()







