# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 18:46:22 2024

@author: siddi
"""

import pickle
import os
import openai
import pandas as pd
import streamlit as st
import gspread
import plotly.graph_objects as go
import plotly.express as px

from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from google.oauth2 import service_account
from datetime import datetime


load_dotenv()
# Access the API key
openai.api_key= os.getenv("OPENAI_API_KEY")

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
# storing data in diabetes google sheets
def store_data_in_google_sheets(data):
    json_file_path = 'danger/diabetes-410815-3fb0f7e88b03.json'
    credentials = service_account.Credentials.from_service_account_file(
        json_file_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    )
    client = gspread.authorize(credentials)
    sheet = client.open("Diabetes-sheet").sheet1  
    date = pd.to_datetime('today').strftime("%Y-%m-%d")
    data_with_date = [date] + data
    sheet.append_row(data_with_date)


if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()


# insert data into diabetes table
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
    selected_data = df.loc[mask].drop('diab_diagnosis', axis=1)

    return selected_data


def get_gpt3_response(diagnosis):
    try:
        prompt = "Provide precautions for a person depending on the following report submitted by him/her:{diagnosis}. Strictly take into account the values entered in Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction and compare them with the normal range they should actually be in to let the person know how much deviation is there. The values that are not in the normal range as they should be then accordinly give the precautions to comeback to normal range. The precautions shall include what the person should eat and also what the person should avoid eating with taking into account the age of the person.Compare the values with normal range they should be in. Start the response with 'The report shows that you are diabetic.....'. End the response with a sweet message to the patient."
        
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct-0914",
            prompt=prompt,
            max_tokens=350,
            temperature=0.95
        )
        if response.choices and response.choices[0].text:
            return response.choices[0].text.strip()
        else:
            return "Unable to generate precautions."

    except Exception as e:
        return f"Error occurred: {str(e)}"



diabetes_model = pickle.load(open('C:/Users/siddi/OneDrive/Desktop/Model/diabetes_model.sav', 'rb'))

heart_disease_model = pickle.load(open('C:/Users/siddi/OneDrive/Desktop/Model/heart_disease_model.sav', 'rb'))


# main sidebar
with st.sidebar:
    selected = option_menu(menu_title=None,
                        options=['Diabetes Analyser',
                            'Heart Disease Analyser'],
                        menu_icon='hospital-fill',
                        icons=['activity', 'heart'],
                        default_index=0)
    st.image("images/Logoo.png")



# Diabetes Prediction Page sidebar
if selected == 'Diabetes Analyser':
    select = option_menu(menu_title=None,
                        options=['Diabetes Report',
                        'Diabetes Analysis'],
                        icons=['pencil-fill','bar-chart-fill'],
                        orientation='horizontal',
                        )
    
# Heart Prediction Page sidebar
if selected == 'Heart Disease Analyser':
    select = option_menu(menu_title=None,
                        options=['Heart Report',
                        'Heart Analysis'],
                        icons=['pencil-fill','bar-chart-fill'],
                        orientation='horizontal',
                        )
    
# diabetes
if select=='Diabetes Report':
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
                    diab_diagnosis = 'The person is diabetic'
                else:
                    diab_diagnosis = 'The person is not diabetic'

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


                if diab_diagnosis == 'The person is diabetic':
                    precautions = get_gpt3_response(diab_diagnosis)
                    st.markdown("### Precautions:")
                    st.write(precautions)


if select=='Diabetes Analysis':

    json_file_path = 'danger/diabetes-410815-3fb0f7e88b03.json'
    credentials = service_account.Credentials.from_service_account_file(
        json_file_path,
        scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(credentials)

    all_data = fetch_data(pd.to_datetime('2023-03-01'), pd.to_datetime('2024-12-30')) 

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

        st.header("Diabetes Report")
        st.write(selected_data)

        if selected_data.empty:
            st.warning("No report available for the selected period.")
        else:
            columns_to_plot = ['Pregnancies','Glucose','BloodPressure', 'BMI','Insulin','DiabetesPedigreeFunction']
            fig = px.line(selected_data, x='Date', y=columns_to_plot, title='Diabetes Progress Over Time')
            fig.update_layout(template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)


# Heart disease prediction
# storing data in heart disease google sheets
def store_data_in_google_sheets(data):
    json_file_path = 'danger/heart-410815-eab8e7b4e4b7.json'
    credentials = service_account.Credentials.from_service_account_file(
        json_file_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    )
    client = gspread.authorize(credentials)
    sheet = client.open("Heart-sheet").sheet1  
    date = pd.to_datetime('today').strftime("%Y-%m-%d")
    data_with_date = [date] + data
    sheet.append_row(data_with_date)


if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()


# insert data into diabetes table
def insert_data(data):
    try:
        json_file_path = 'danger/heart-410815-eab8e7b4e4b7.json'
        credentials = service_account.Credentials.from_service_account_file(
        json_file_path,
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        client = gspread.authorize(credentials)
        sheet = client.open("Heart-sheet").sheet1  
        current_date = datetime.now().strftime("%Y-%m-%d")
        data_with_date = [current_date] + data
        sheet.append_row(data_with_date) 
        st.success("Data inserted successfully.")
    except Exception as e:
        st.error(f"Error inserting data: {e}")


# Function to fetch data from Google Sheets based on the selected period
def fetch_data(selected_start_date, selected_end_date):
    sheet = client.open("Heart-sheet").sheet1 
    all_data = sheet.get_all_records()

    df = pd.DataFrame(all_data)

    df['Date'] = pd.to_datetime(df['Date'])
    mask = (df['Date'] >= selected_start_date) & (df['Date'] <= selected_end_date)
    selected_data = df.loc[mask].drop('heart_diagnosis', axis=1)

    sex_mapping = {0: 'Male', 1: 'Female'}
    selected_data['sex'] = selected_data['sex'].map(sex_mapping)

    

    return selected_data


    
if select =='Heart Report':
    with st.form("entry_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.text_input('Age')

        with col2:
            sex = st.text_input('Sex')
            if sex=='Female':
                sex=1
            if sex=='female':
                sex=1
            if sex=='Male':
                sex=0
            else: sex=0

        with col3:
            cp = st.text_input('Chest Pain')

        with col1:
            trestbps = st.text_input('Resting Blood Pressure')

        with col2:
            chol = st.text_input('Serum Cholestoral')

        with col3:
            fbs = st.text_input('Fasting Blood Sugar')

        with col1:
            restecg = st.text_input('Resting Electrocardiographic')

        with col2:
            thalach = st.text_input('Maximum Heart Rate')

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

        heart_diagnosis = ''

        # creating a button for Prediction
        submitted=st.form_submit_button('Heart Test Result')
    if submitted:

        user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]


        user_input = [float(x) for x in user_input]

        heart_prediction = heart_disease_model.predict([user_input])

        if heart_prediction[0] == 1:
            heart_diagnosis = 'The person is having heart disease'
        else:
            heart_diagnosis = 'The person does not have any heart disease'

        data_to_insert = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal,heart_diagnosis] 
        insert_data(data_to_insert)


        # Store the input values in session_state
        st.session_state.heart_data = {
            "age":age,
            "sex":sex,
            "cp":cp,
            "trestbps":trestbps,
            "chol":chol,
            "fbs":fbs,
            "restecg":restecg,
            "thalach":thalach,
            "exang":exang,
            "oldpeak":oldpeak,
            "slope":slope,
            "ca":ca,
            "thal":thal,
            "Diagnosis": heart_diagnosis

        }

        st.success(heart_diagnosis)
        if hasattr(st.session_state, 'heart_data'):
            heart_data = pd.DataFrame(st.session_state.heart_data, index=[0])
            st.dataframe(heart_data)
            fig = go.Figure(data=[go.Pie(labels=heart_data.columns, values=heart_data.iloc[0].values)])
            st.plotly_chart(fig, use_container_width=True)

if select=='Heart Analysis':

    json_file_path = 'danger/heart-410815-eab8e7b4e4b7.json'
    credentials = service_account.Credentials.from_service_account_file(
        json_file_path,
        scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(credentials)

    all_data = fetch_data(pd.to_datetime('2023-03-01'), pd.to_datetime('2024-12-30')) 

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

        st.header("Heart Report")
        st.write(selected_data)

        if selected_data.empty:
            st.warning("No report available for the selected period.")
        else:
            columns_to_plot = ['cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
            fig = px.line(selected_data, x='Date', y=columns_to_plot, title='Heart Progress Over Time')
            fig.update_layout(template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
