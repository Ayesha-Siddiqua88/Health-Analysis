# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 19:21:27 2024

@author: siddi
"""
import streamlit as st

page_bg_img="""
<style>
[data-testid="stAppViewContainer"]{
background: linear-gradient(180deg, #000000, #0e2228)
}
</style>
"""
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown(page_bg_img,unsafe_allow_html=True)

st.title("Main Page")

