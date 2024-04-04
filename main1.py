
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

SUPABASE_KEY=os.getenv('SUPERBASE_KEY')
SUPABASE_URL=os.getenv('SUPERBASE_URL')

supabase : Client = create_client(SUPABASE_URL,SUPABASE_KEY)

details = {
    'invoice_date': '2022-01-01',
    'user_id': 3,
    'invoice_id': 5678,
    'invoice_name': 'Example Invoice',
    'invoice_company': 'ABC Company',
    'invoice_number': 56789,
    'total_amount': 1000,
    'no_of_items': 5,
    'invoices_user_id': "2" + "_" + '1'
}

supabase.table("Invoices").insert({
    "invoice_date": details['invoice_date'],
    "user_id": 3,
    "invoice_id": details['invoice_number'],
    "invoice_name": details['invoice_name'],
    "invoice_company": details['invoice_company'],
    "invoice_no": details['invoice_number'],
    "total_amount": int(details['total_amount']),
    "no_of_items": int(details['no_of_items']),
    "invoices_user_id": details['invoices_user_id'],
}).execute()