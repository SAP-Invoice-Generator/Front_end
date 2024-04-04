from supabase import create_client
import os
from dotenv import load_dotenv
load_dotenv()
SUPABASE_KEY=os.getenv('SUPERBASE_KEY')
SUPABASE_URL=os.getenv('SUPERBASE_URL')

supabase  = create_client(SUPABASE_URL,SUPABASE_KEY)

path=r"C:\Users\harec\Downloads\SAP ground work\train\invoice\Invoice_9_affine_translation_jpg.rf.7153a8ec6cb8c514b0e4ebc7b7fd2eb2.jpg"

# Store the PDF file in the Supabase bucket
response = supabase.storage.from_('invoice_bucket').upload("sample1.jpeg",path,{"content-type":"image/jpeg"})

# Check if the upload was successful
print(response)