import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import gspread
import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from supabase import create_client, Client 
from postgrest.exceptions import APIError
import time

load_dotenv()

CREDENTIALS_JSON = os.getenv('CREDENTIALS_JSON')
SHEET_KEY=os.getenv('SHEET_KEY')
GEMINI_KEY=os.getenv('GEMINI_KEY')
SUPABASE_KEY=os.getenv('SUPERBASE_KEY')
SUPABASE_URL=os.getenv('SUPERBASE_URL')

supabase : Client = create_client(SUPABASE_URL,SUPABASE_KEY)

gc = gspread.service_account(filename=CREDENTIALS_JSON)
sheet = gc.open_by_key(SHEET_KEY)
worksheet = sheet.sheet1

# Ensure the API key is configured
genai.configure(api_key=GEMINI_KEY)
model1 = genai.GenerativeModel('gemini-pro')
model2 = genai.GenerativeModel('gemini-pro-vision')




class MyApp:
    def __init__(self):
        self.username = None
    
    def login(self):
        st.title("Login New")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            # Retrieve user and password from Supabase
            users = supabase.table('users').select('username, password').execute()
            
            # Check if username and password match
            if any(user['username'] == username and user['password'] == password for user in users):
                self.username = username
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password")
        
        if st.button("Register"):
            # Redirect to register page
            st.write("Redirecting to register page...")
            # Add your code to redirect to the register page here
    
    def main(self):
        self.login()
        # Add your code for other pages here

if __name__ == "__main__":
    app = MyApp()
    app.main()