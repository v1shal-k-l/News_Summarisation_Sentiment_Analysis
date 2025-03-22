## Import Libraries
from fastapi import FastAPI
from pydantic import BaseModel
from main import analyze_company_news

## Initialize FastAPI
app = FastAPI()

## Company Request Model
class CompanyRequest(BaseModel):
    Company_Name: str

## API Endpoint
@app.post("/api/company")
async def handle_company(request: CompanyRequest):
    company = request.Company_Name.strip()
    result = analyze_company_news(company)
    return result

## Run API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)