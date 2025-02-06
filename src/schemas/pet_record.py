from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class PetRecordBase(BaseModel):
    title: str
    description: str
    pet_name: str
    record_date: datetime
    image_urls: List[str]
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PetRecordCreate(PetRecordBase):
    pass

class PetRecordUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    pet_name: Optional[str] = None
    record_date: Optional[datetime] = None
    image_urls: Optional[List[str]] = None

class PetRecord(PetRecordBase):
    id: str = Field(alias="_id")

    class Config:
        allow_population_by_field_name = True