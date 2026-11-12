import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

# 1. Initialize the API Engine
app = FastAPI()

# 2. Configure Security Permissions (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits your GitHub Pages frontend to request data
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Connect to Your Cloud Database
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 4. The Visitor Counter Route
@app.get("/visit")
def update_visitor_count():
    # Fetch the current count from row 1
    result = supabase.table("visitor_counter").select("count").eq("id", 1).execute()
    current_count = result.data[0]["count"]
    
    # Add 1 to the count
    new_count = current_count + 1
    
    # Save the updated number back to Supabase
    supabase.table("visitor_counter").update({"count": new_count}).eq("id", 1).execute()
    
    # Return the new number as JSON data
    return {"visitor_count": new_count}
