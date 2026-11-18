from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class SalesRecordBase(BaseModel):
    product_name: str
    quantity_sold: int
    revenue: float

class SalesRecordResponse(SalesRecordBase):
    id:int
    upload_timestamp:datetime

    model_config = ConfigDict(from_attributes=True)

class MerchantBase(BaseModel):
    company_name:str

class MerchantCreate(MerchantBase):
    password:str

class MerchantResponse(MerchantBase):
    id:int
    sales: List[SalesRecordResponse] = []
    model_config = ConfigDict(from_attributes = True)
    