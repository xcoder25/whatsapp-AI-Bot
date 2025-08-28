from pydantic import BaseModel, Field

class SendTextRequest(BaseModel):
    to: str = Field(..., description="E.164 phone, e.g., 2348012345678")
    body: str
