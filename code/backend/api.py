from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transaction_service import TransactionService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

transaction_service = TransactionService()

class TransactionRequest(BaseModel):
    account_id: str
    transaction_type: str
    amount: float

@app.post("/transaction/")
async def handle_transaction(request: TransactionRequest):
    response = transaction_service.process_transaction(
        request.account_id, request.transaction_type, request.amount
    )
    return response
