# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 18:46:22 2024

@author: siddi
"""

from datetime import datetime
import pickle
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import gspread
import plotly.express as px
from google.oauth2 import service_account

# styling
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# diabetes section
# storing data in google sheets
def store_data_in_google_sheets(data):
    json_file_path = 'danger/diabetes-410815-3fb0f7e88b03.json'
    credentials = service_account.Credentials.from_service_account_file(
        json_file_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    )
    client = gspread.authorize(credentials)
    sheet = client.open("Diabetes-sheet").sheet1  # Replace "DiabetesData" with your sheet title
    date = pd.to_datetime('today').strftime("%Y-%m-%d")
    data_with_date = [date] + data
    sheet.append_row(data_with_date)


# insert data into table
def insert_data(data):
    try:
        json_file_path = 'danger/diabetes-410815-3fb0f7e88b03.json'
        credentials = service_account.Credentials.from_service_account_file(
        json_file_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        client = gspread.authorize(credentials)
        sheet = client.open("Diabetes-sheet").sheet1  
        current_date = datetime.now().strftime("%Y-%m-%d")
        data_with_date = [current_date] + data
        sheet.append_row(data_with_date) 
        st.success("Data inserted successfully.")
    except Exception as e:
        st.error(f"Error inserting data: {e}")




# Function to fetch data from Google Sheets based on the selected period
def fetch_data(selected_start_date, selected_end_date):
    sheet = client.open("Diabetes-sheet").sheet1 
    all_data = sheet.get_all_records()

    df = pd.DataFrame(all_data)

    df['Date'] = pd.to_datetime(df['Date'])
    mask = (df['Date'] >= selected_start_date) & (df['Date'] <= selected_end_date)
    selected_data = df.loc[mask]

    return selected_data



diabetes_model = pickle.load(open('C:/Users/siddi/OneDrive/Desktop/Model/diabetes_model.sav', 'rb'))

heart_disease_model = pickle.load(open('C:/Users/siddi/OneDrive/Desktop/Model/heart_disease_model.sav', 'rb'))




# main sidebar
with st.sidebar:
    selected = option_menu('Disease Prediction System',

                           ['Diabetes Prediction',
                            'Heart Disease Prediction'],
                           menu_icon='hospital-fill',
                           icons=['activity', 'heart'],
                           default_index=0)


# Diabetes Prediction Page sidebar
if selected == 'Diabetes Prediction':
    select = option_menu(menu_title=None,
                         options=['Data Entry',
                          'Data Visualization'],
                         icons=['pencil-fill','bar-chart-fill'],
                         orientation='horizontal',
                           )
if select=='Data Entry':
  st.header("Data Entry")
  with st.form("entry_form", clear_on_submit=True):
    # getting the input data from the user
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

    # creating a button for Prediction
            submitted=st.form_submit_button('Diabetes Test Result')
            if submitted:
        
                user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin,
                            BMI, DiabetesPedigreeFunction, Age]

                user_input = [float(x) for x in user_input]

                diab_prediction = diabetes_model.predict([user_input])

                if diab_prediction[0] == 1:
                    diab_diagnosis = 'The person is diabetic'
                else:
                    diab_diagnosis = 'The person is not diabetic'

                data_to_insert = [Pregnancies, Glucose, BloodPressure,SkinThickness, Insulin,BMI, DiabetesPedigreeFunction,Age,diab_diagnosis] 
                insert_data(data_to_insert)

                # Store the input values in session_state
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


if select=='Data Visualization':
    st.header("Data Visualization")
    
    if hasattr(st.session_state, 'diabetes_data'):
        json_file_path = 'danger/diabetes-410815-3fb0f7e88b03.json'
        credentials = service_account.Credentials.from_service_account_file(
            json_file_path,
            scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        )
        client = gspread.authorize(credentials)

        all_data = fetch_data(pd.to_datetime('2023-03-01'), pd.to_datetime('2024-12-30'))  # Use an initial wide date range

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

            st.write(f"Selected Period: {selected_starting_date.strftime('%Y-%m-%d')} to {selected_ending_date.strftime('%Y-%m-%d')}")

            selected_data = fetch_data(selected_starting_date, selected_ending_date)

            if selected_data.empty:
                st.warning("No data available for the selected period.")
            else:
                columns_to_plot = ['Pregnancies', 'BMI', 'Insulin']
                fig = px.line(all_data, x='Date', y=columns_to_plot, title='Diabetes Progress Over Time')
                st.plotly_chart(fig, use_container_width=True)



    

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':

    # page title
    st.title('Heart Disease Prediction using ML')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age')

    with col2:
        sex = st.text_input('Sex')

    with col3:
        cp = st.text_input('Chest Pain types')

    with col1:
        trestbps = st.text_input('Resting Blood Pressure')

    with col2:
        chol = st.text_input('Serum Cholestoral in mg/dl')

    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')

    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')

    with col3:
        exang = st.text_input('Exercise Induced Angina')

    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')

    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')

    with col3:
        ca = st.text_input('Major vessels colored by flourosopy')

    with col1:
        thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

    # code for Prediction
    heart_diagnosis = ''

    # creating a button for Prediction

    if st.button('Heart Disease Test Result'):

        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

        user_input = [float(x) for x in user_input]

        heart_prediction = heart_disease_model.predict([user_input])

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person is having heart disease'
        else:
            heart_diagnosis = 'The person does not have any heart disease'

    st.success(heart_diagnosis)

