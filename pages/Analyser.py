import pickle
import pandas as pd
import streamlit as st
import gspread
import plotly.graph_objects as go
import plotly.express as px

from streamlit_option_menu import option_menu
from google.oauth2 import service_account
from datetime import datetime

# styling
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

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


# diabetes section
# storing data in diabetes google sheets
def store_data_in_google_sheets(data):
    json_file_path = 'danger/diabetes.json'
    credentials = service_account.Credentials.from_service_account_file(
        json_file_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    )
    client = gspread.authorize(credentials)
    sheet = client.open("Diabetes spreadsheet").sheet1  
    date = pd.to_datetime('today').strftime("%Y-%m-%d")
    data_with_date = [date] + data
    sheet.append_row(data_with_date)


if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()


# insert data into diabetes table
def insert_data(data):
    try:
        json_file_path = 'danger/diabetes\.json'
        credentials = service_account.Credentials.from_service_account_file(
        json_file_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        client = gspread.authorize(credentials)
        sheet = client.open("Diabetes spreadsheet").sheet1  
        current_date = datetime.now().strftime("%Y-%m-%d")
        data_with_date = [current_date] + data
        sheet.append_row(data_with_date) 
    except Exception as e:
        st.error(f"Error inserting data: {e}")


# Function to fetch data from Google Sheets based on the selected period
def fetch_data(selected_start_date, selected_end_date):
    sheet = client.open("Diabetes spreadsheet").sheet1 
    all_data = sheet.get_all_records()

    df = pd.DataFrame(all_data)

    df['Date'] = pd.to_datetime(df['Date'])
    mask = (df['Date'] >= selected_start_date) & (df['Date'] <= selected_end_date)
    selected_data = df.loc[mask].drop('diab_diagnosis', axis=1)

    return selected_data

# loading the trained ml models
diabetes_model = pickle.load(open('Model/diabetes_model.sav', 'rb'))

# main sidebar
with st.sidebar:
    selected = option_menu(menu_title=None,
                        options=['Diabetes Analyser'],
                        menu_icon='hospital-fill',
                        icons=['activity'],
                        default_index=0)
    st.image("images/Logo.png")

# Diabetes Prediction Page sidebar
if selected == 'Diabetes Analyser':
    select = option_menu(menu_title=None,
                        options=['Diabetes Report',
                        'Diabetes Analysis'],
                        icons=['pencil-fill','bar-chart-fill'],
                        orientation='horizontal',
                        )
        
# Diabetes Report entry
if select=='Diabetes Report':
    st.write("In the Diabetes Report section, you can enter various health parameters to receive an assessment of your diabetes status. "
             "Based on the input, we’ll provide a recommendation to help you understand your current health condition.")
    with st.form("entry_form", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)

            with col1:
                Pregnancies = st.text_input('Number of Pregnancies')

            with col2:
                Glucose = st.text_input('Glucose Level')

            with col3:
                BloodPressure = st.text_input('Blood Pressure value')

            with col1:
                SkinThickness = st.text_input('Skin Thickness value')

            with col2:
                Insulin = st.text_input('Insulin Level')

            with col3:
                BMI = st.text_input('BMI value')

            with col1:
                DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

            with col2:
                Age = st.text_input('Age of the Person')


            diab_diagnosis = ''
            submitted=st.form_submit_button('Diabetes Test Result')
            if submitted:
        
                user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                            BMI, DiabetesPedigreeFunction, Age]

                user_input = [float(x) for x in user_input]

                diab_prediction = diabetes_model.predict([user_input])

                if diab_prediction[0] == 1:
                    diab_diagnosis = 'According to the report entered, you are diabetic'
                else:
                    diab_diagnosis = 'According to the report entered, you are not diabetic'

                data_to_insert = [Pregnancies, Glucose, BloodPressure,SkinThickness, Insulin,BMI, DiabetesPedigreeFunction,Age,diab_diagnosis] 
                insert_data(data_to_insert)

                st.session_state.diabetes_data = {
                    "Pregnancies": Pregnancies,
                    "Glucose": Glucose,
                    "BloodPressure": BloodPressure,
                    "SkinThickness": SkinThickness,
                    "Insulin": Insulin,
                    "BMI": BMI,
                    "DiabetesPedigreeFunction": DiabetesPedigreeFunction,
                    "Age": Age,
                    "Diagnosis": diab_diagnosis
                }


                st.success(diab_diagnosis)
                if hasattr(st.session_state, 'diabetes_data'):
                    diabetes_data = pd.DataFrame(st.session_state.diabetes_data, index=[0])
                    st.dataframe(diabetes_data)
                    fig = go.Figure(data=[go.Pie(labels=diabetes_data.columns, values=diabetes_data.iloc[0].values)])
                    st.plotly_chart(fig, use_container_width=True)


# Diabetes Analysis section
if select=='Diabetes Analysis':

    st.write("In the Diabetes Analysis section, you can view trends and patterns in your diabetes-related health data over time. "
             "Select a time period to analyze how key health indicators have changed.")

    json_file_path = 'danger/diabetes.json'
    credentials = service_account.Credentials.from_service_account_file(
        json_file_path,
        scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(credentials)

    all_data = fetch_data(pd.to_datetime('2024-11-03'), pd.to_datetime('2024-12-30')) 

    if all_data.empty:
        st.warning("No data available.")
    else:
        unique_dates = sorted(all_data['Date'].dt.strftime('%Y-%m-%d').unique())

    if not unique_dates:
        st.warning("No unique dates found.")
    else:
        start_date = st.selectbox("Select Start Date:", unique_dates)
        end_date = st.selectbox("Select End Date:", unique_dates)

        selected_starting_date = pd.to_datetime(start_date)
        selected_ending_date = pd.to_datetime(end_date)

        selected_data = fetch_data(selected_starting_date, selected_ending_date)

        st.title("Diabetes Variation")
        st.write(selected_data)

        if selected_data.empty:
            st.warning("No report available for the selected period.")
        else:
            columns_to_plot = ['Pregnancies','Glucose','BloodPressure', 'BMI','Insulin','DiabetesPedigreeFunction']
            fig = px.line(selected_data, x='Date', y=columns_to_plot, title='Diabetes Progress Over Time')
            fig.update_layout(template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)


# insert data into diabetes table
def insert_data(data):
    try:
        json_file_path = 'danger/diabetes.json'
        credentials = service_account.Credentials.from_service_account_file(
        json_file_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        client = gspread.authorize(credentials)
        sheet = client.open("Diabetes spreadsheet").sheet1  
        current_date = datetime.now().strftime("%Y-%m-%d")
        data_with_date = [current_date] + data
        sheet.append_row(data_with_date) 
    except Exception as e:
        st.error(f"Error inserting data: {e}")
