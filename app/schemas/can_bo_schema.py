from pydantic import BaseModel
from typing import Optional


class CanBoResponse(BaseModel):
    id: int
    ho_ten: str
    chuc_vu: Optional[str] = None

    class Config:
        from_attributes = True
