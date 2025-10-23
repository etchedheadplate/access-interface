import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

app = FastAPI()

DB_SERVICE_API_URL = str(os.environ.get("DB_SERVICE_API_URL"))


@app.get("/ping_db")
async def send_ping():
    async with httpx.AsyncClient() as client:
        response = await client.get(DB_SERVICE_API_URL + "/ping")
        return {"from_db_service": response.json()}
