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






class gemini_model:
    def __init__(self):
       
        self.response_dict = {}  # Make response_dict a class attribute
        self.details = []  # Make details a class attribute
        self.input_prompt = """
            You are an expert in understanding invoices.
            You will receive input images as invoices & text
            you will have to answer questions based on the input image
            """
     
    # Function to get the response for PDF input
    def get_gemini_response_pdf(self,input_prompt, context):
        response = model1.generate_content([context, input_prompt])
        return response.text

    # Function to get the response for image input
    def get_gemini_response_image(self,input, image, prompt):
        response = model2.generate_content([input, image[0], prompt])
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




    def main_model(self):


        input = '''give me the details of the invoice like invoice name, invoice number as a integer,invoice company, date, total amount as a integer , no of items as a integer, 
        i need only these fields do not give me any extra details ok?  
        if any field is not available, return them as NULL,
        i need all detials as a python dictionary  '''

        # Dynamic rows to store details
        details = []

        uploaded_file = st.file_uploader("Upload an image or PDF...", type=["jpg", "jpeg", "png", "pdf"])
        submit = st.button("Tell me about it")

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
                print(response)

                respons_lst = response.split("\n")
                # for x in response:
                #     respons_lst.append(x)
                print(respons_lst)
                for i in respons_lst[:-1]:
                    if i not in ['{','}',"'","```"]:
                        details.append(i)
                details.pop(0)
                details = [str(x) for x in details]
                st.write(response)
                print(details)
                response_dict = {}
                for x in details:
                    key,val = x.split(':',1)
                    key = key.strip().strip('"')
                    key=key.replace(":","")
                    val=val.replace(",","")
                    print(key," corresponding value is ",val)
                    response_dict[key] = val
                
                values = []
                for key, value in response_dict.items():
                    value = value.replace('"', "")
                    st.text_input(key, value)
                    values.append(value)
                worksheet.append_row(values)
                    
                print(response_dict)
                try:
                    supabase.table("Invoices").insert({
                        "invoice_id": int(response_dict['invoice_number']), 
                        "invoice_name": response_dict['invoice_name'],
                        # "date":response_dict['date'], 
                        "invoice_company":response_dict['invoice_company'],
                        "invoice_no": int(response_dict['invoice_number']),   
                        "total_amount":int(response_dict['total_amount']),  
                        "no_of_items":int(response_dict['no_of_items'])
                    }).execute()
                except APIError as e:
                    if '23505' in str(e): 
                        st.error('This invoice has already been uploaded.')
                    else:
                        raise  
##########################################################################################################
username = ""
password = ""

class user_interface:
    def __init__(self):
        self.username = ""
        self.password = ""
    def authenticate_and_get_user_id(self, username, password):
        try:
            data = supabase.table("Users").select("user_id").eq("username", username).eq("password", password).execute()

            if data.data:
                # Assuming the first match is the correct one since usernames should be unique
                user_id = data.data[0]['user_id']
                return True, user_id  # Return both authentication success and user_id
            else:
                return False, None
        except Exception as e:
            print(f"An error occurred during authentication: {e}")
            return False, None

        # Function to create login page
    def login_page(self):
        st.title("Login")
        self.username = st.text_input("Username")
        self.password = st.text_input("Password", type="password")
        login_button = st.button("Login")

        if login_button:
            authenticated, user_id = self.authenticate_and_get_user_id(self.username, self.password)
            if authenticated:
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = user_id  # Store the user_id in the session state
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
    def fetch_user_profile(self, user_id):
        try:
            data = supabase.table("Users").select("*").eq("user_id", user_id).execute()

            # Check if data was found
            if data.data:
                user_data = data.data[0]  # Assuming user_id is unique, hence taking the first match
                # Format the user data dictionary
                formatted_user_data = {
                    'name': user_data['username'],  # Assuming you want to use username as name
                    'email': user_data['email'],
                    'phone_number': user_data['phone_no'],
                    'username': user_data['username'],
                    'address': user_data['address'],
                    # Provide a default or specific URL for the profile photo if it's not stored in the database
                    'profile_photo_url': 'https://picsum.photos/200/300?random=1'
                }
                return formatted_user_data
            else:
                # Handle case where no user is found
                return {
                    'name': 'User not found',
                    'email': '',
                    'phone_number': '',
                    'username': '',
                    'address': '',
                    'profile_photo_url': 'https://picsum.photos/200/300?random=2'  # URL to a default profile photo
                }
        except Exception as e:
            print(f"An error occurred: {e}")
            return {
                'name': 'Error fetching profile',
                'email': '',
                'phone_number': '',
                'username': '',
                'address': '',
                'profile_photo_url': 'https://picsum.photos/200/300?random=3'  # URL to an error profile photo
            }


        # Function to display profile page
    def display_profile_page(self):
            # Fetch user profile data
            user_id = st.session_state.user_id 
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
            selected = option_menu(
                menu_title=None,
                options=["Home", "Profile", "Invoices", "Upload New Invoice", "Logout"]
            )
            
           
            
            
            # st.sidebar.title("Menu")
            if selected == "Home":
                st.session_state.page = 'home'
            if selected == "Profile":
                st.session_state.page = 'profile'
            if selected == "Invoices":
                st.session_state.page = 'invoices'
            if selected == "Upload New Invoice":
                st.session_state.page = 'upload_invoice'
            if selected == "Logout":
                st.session_state.logged_in = False
                st.session_state.page = 'login'

        # st.session_state.sync()  # Add this line to sync session state changes

        if st.session_state.page == 'home':
            ui.home_page()
        elif st.session_state.page == 'profile':
            st.title('User Profile Page')
            ui.display_profile_page()
        elif st.session_state.page == 'invoices':
            ui.invoice_main()
            # st.title("Invoice page")
        elif st.session_state.page == 'upload_invoice':
            st.header("Upload Your Invoice")
            g_model.main_model()
            # ui.upload_invoice_page()


# Run the main function
if __name__ == "__main__":
    main()

