import os
from dotenv import load_dotenv, find_dotenv

print("CWD:", os.getcwd())
print("DOTENV FOUND AT:", find_dotenv())

print("Before load:", os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

load_dotenv()

print("After load:", os.getenv("SUPABASE_SERVICE_ROLE_KEY"))