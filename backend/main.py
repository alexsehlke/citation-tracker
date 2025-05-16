from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CitationRequest(BaseModel):
    api_key: str
    dois: list[str]

@app.post("/api/citations")
def fetch_citations(payload: CitationRequest):
    results = {}
    for doi in payload.dois:
        url = f"https://api.elsevier.com/content/abstract/doi/{doi}"
        headers = {
            "X-ELS-APIKey": payload.api_key,
            "Accept": "application/json"
        }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            results[doi] = r.json()
        else:
            results[doi] = {"error": f"Failed with status {r.status_code}"}
        time.sleep(1)  # Respect rate limits
    return results

# Optional for local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)