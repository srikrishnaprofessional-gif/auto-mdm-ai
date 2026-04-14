from fastapi import FastAPI
from app.agent import run_agent

app = FastAPI()

@app.get("/run-agent")
def run():
    df, report = run_agent()
    return {"status": "success", "report": report}