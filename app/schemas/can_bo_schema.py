from pydantic import BaseModel
from typing import Optional


class CanBoResponse(BaseModel):
    id: int
    ho_ten: str
    chuc_vu: Optional[str] = None

    class Config:
        from_attributes = True
        
from pydantic import BaseModel

class CanBoCreate(BaseModel):
    # Cậu dán tạm cái này vào để Python nó nhận diện trước nha
    pass

class CanBoUpdate(CanBoCreate):
    pass