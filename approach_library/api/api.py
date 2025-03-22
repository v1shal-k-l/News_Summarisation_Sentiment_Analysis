# Importing Libraries
from fastapi import FastAPI
from pydantic import BaseModel
from main import analyze_company_news  # Import the function from main.py

# Initialize FastAPI
app = FastAPI()

# Defining the CompanyRequest model
class CompanyRequest(BaseModel):
    Company_Name: str

# Defining the API endpoint
@app.post("/api/company")
async def handle_company(request: CompanyRequest):
    company = request.Company_Name.strip()
    result = analyze_company_news(company)
    return result

## Run API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)