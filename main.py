import streamlit as st
import google.generativeai as genai
from PIL import Image
from PyPDF2 import PdfReader
import gspread
import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# r={"invoice_name":[],"invoice_number":[],"invoice_number":[],"invoice_date":[],'total_amount':[],'no_of_items':[]}







class gemini_model:
    def __init__(self):
        load_dotenv()

        CREDENTIALS_JSON = os.getenv('CREDENTIALS_JSON')
        SHEET_KEY = os.getenv('SHEET_KEY')
        GEMINI_KEY = os.getenv('GEMINI_KEY')

        gc = gspread.service_account(filename=CREDENTIALS_JSON)
        sheet = gc.open_by_key(SHEET_KEY)
        self.worksheet = sheet.sheet1  # Make worksheet a class attribute

        # Ensure the API key is configured
        genai.configure(api_key=GEMINI_KEY)
        self.model1 = genai.GenerativeModel('gemini-pro')  # Make model1 a class attribute
        self.model2 = genai.GenerativeModel('gemini-pro-vision')  # Make model2 a class attribute
        self.response_dict = {}  # Make response_dict a class attribute
        self.details = []  # Make details a class attribute
        
    def get_gemini_response_pdf(self,input_prompt, context):
            response = self.model1.generate_content([context, input_prompt])
            return response.text

        # Function to get the response for image input
    def get_gemini_response_image(self,input, image, prompt):
            response = self.model2.generate_content([input, image[0], prompt])
            return response.text

        # Function to extract text from PDF
    def get_pdf_text(self,pdf_docs):
            text = ""
            for pdf in pdf_docs:
                pdf_reader = PdfReader(pdf)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text

        # Function to set up image data for processing
    def input_image_setup(self,uploaded_file):
            if uploaded_file is not None:
                bytes_data = uploaded_file.getvalue()
                image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
                return image_parts
            else:
                raise FileNotFoundError("No file uploaded")


    input_prompt = """
                    You are an expert in understanding invoices.
                    You will receive input images as invoices & text
                    you will have to answer questions based on the input image
                    """
    
    def main_model(self):
        st.header("Upload your Invoice")

        input = '''give me the details of the invoice like invoice name, invoice number,invoice company, date, total amount, no of items, 
        i need only these fields do not give me any extra details ok?  
        if any field is not available, return them as NULL,
        i need all details as a python dictionary  '''

        uploaded_file = st.file_uploader("Upload an image or PDF...", type=["jpg", "jpeg", "png", "pdf"])
        submit = st.button("Upload")

        if uploaded_file is not None:
            if uploaded_file.type.startswith('image/'):
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image.", use_column_width=True)
                image_data = self.input_image_setup(uploaded_file)
                response = self.get_gemini_response_image(self.input_prompt, image_data, input)
            elif uploaded_file.type == 'application/pdf':
                st.write("Uploaded PDF:", uploaded_file.name)
                image = None
                context = self.get_pdf_text([uploaded_file])
                response = self.get_gemini_response_pdf(input, context)
            else:
                raise ValueError("Unsupported file type.")

            if submit:
                details = []
                st.subheader("The Response is")
                response = response.replace("python","")
                # print(response)

                respons_lst = response.split("\n")
                # for x in response:
                #     respons_lst.append(x)
                # print(respons_lst)
                for i in respons_lst[:-1]:
                    if i not in ['{','}',"'","```"]:
                        details.append(i)
                details.pop(0)
                details = [str(x) for x in details]
                st.write(response)
                # print(details)
                response_dict = {}
                for x in details:
                    key,val = x.split(':',1)
                    key = key.strip().strip('"')
                    key=key.replace(":","")
                    val=val.replace(",","")
                    # print(key," corresponding value is ",val)
                    response_dict[key] = val
                values = []
                for key, value in response_dict.items():
                    value = value.replace('"', "")
                    st.text_input(key, value)
                    values.append(value)
                self.worksheet.append_row(values)
            
            
            
                


class user_interface:
    def __init__(self):
        pass
    def authenticate(self,username, password):
    # Dummy authentication, replace with actual logic
        if username == 'user' and password == 'password':
            return True
        else:
            return False

        # Function to create login page
    def login_page(self):
            st.title("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.button("Login")

            if login_button and not st.session_state.get('logged_in', False):
                if self.authenticate(username, password):
                    st.session_state.logged_in = True
                    st.session_state.page = 'home'  # Redirect to home page after login
                    st.success("Login successful!")
                else:
                    st.error("Invalid username or password.")

            # Link for new users to register
            if st.session_state.page == 'login':
                if st.button("Register"):
                    st.session_state.page = 'register'

        # Function to create registration page
    def registration_page(self):
            st.title("Registration")
            name = st.text_input("Name", key="name_input")
            email = st.text_input("Email", key="email_input")
            username = st.text_input("Username", key="username_input")
            password = st.text_input("Password", type="password", key="password_input")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password_input")
            
            # Unique key for the Register button
            register_button = st.button("Register", key="register_button")

            # Add a "Back to Login" button
            back_to_login_button = st.button("Back to Login")

            if register_button:
                if not name or not email or not username or not password or not confirm_password:
                    st.error("Please fill in all registration details.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    # Save user data to the database (replace with actual database operation)
                    # Here you would typically save the user's information to your database
                    st.success("Registration successful! You will be redirected to the login page shortly.")
                    # Redirect to login page after successful registration
                    st.session_state.page = 'login'
            
            # Redirect back to login page if "Back to Login" button is clicked
            if back_to_login_button:
                st.session_state.page = 'login'

        # Function to fetch user profile data from backend database
    def fetch_user_profile(self,user_id):
            # Dummy data, replace with actual database query
            user_data = {
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone_number': '+1234567890',
                'username': 'johndoe',
                'address': '123 Main St, City, Country',
                'profile_photo_url': 'https://picsum.photos/200/300?random=1'  # URL to profile photo
            }
            return user_data

        # Function to display profile page
    def display_profile_page(self,user_id):
            # Fetch user profile data
            user_data = self.fetch_user_profile(user_id)

            # Display profile photo
            st.image(user_data['profile_photo_url'], caption='Profile Photo', width=100)

            # Display user information
            st.subheader('User Information')
            st.write(f"**Name:** {user_data['name']}")
            st.write(f"**Email:** {user_data['email']}")
            st.write(f"**Phone Number:** {user_data['phone_number']}")
            st.write(f"**Username:** {user_data['username']}")
            st.write(f"**Address:** {user_data['address']}")
    def home_page(self):
        st.title("Welcome to Invoice Management Tool")

    def invoice_main(self):
        st.title("Invoice pages")

# Main function to run the Streamlit app
# Main function to run the Streamlit app
def main():
    st.set_page_config(page_title="Gemini Demo")
    ui = user_interface()
    g_model = gemini_model()
    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        if st.session_state.page == 'login':
            ui.login_page()
        elif st.session_state.page == 'register':
            ui.registration_page()
    else:
        with st.sidebar:
            st.sidebar.title("Menu")
            if st.sidebar.button("Home"):
                st.session_state.page = 'home'
            if st.sidebar.button("Profile"):
                st.session_state.page = 'profile'
            if st.sidebar.button("Invoices"):
                st.session_state.page = 'invoices'
            if st.sidebar.button("Upload New Invoice"):
                st.session_state.page = 'upload_invoice'
            if st.sidebar.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.page = 'login'

        if st.session_state.page == 'home':
            ui.home_page()
        elif st.session_state.page == 'profile':
            st.title('User Profile Page')
            user_id = 1  # Placeholder for user ID, replace with actual user ID
            ui.display_profile_page(user_id)
        elif st.session_state.page == 'invoices':
            ui.invoice_main()
            # st.title("Invoice page")
        elif st.session_state.page == 'upload_invoice':
            g_model.main_model()
            # ui.upload_invoice_page()

# Run the main function
if __name__ == "__main__":
    main()

