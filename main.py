from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SheetPayload(BaseModel):
    sheet_name: str
    data: List[Dict[str, str]]

@app.post("/upload-sheet/")
async def upload_sheet(payload: SheetPayload):
    print(f"Received sheet: {payload.sheet_name}")
    print(f"Rows: {len(payload.data)}")
    print(payload)
    return {"status": "success", "rows_received": len(payload.data)}
