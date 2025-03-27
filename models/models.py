from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class JsonCategory(BaseModel):
    id_user: int
    name_category: str

class JsonStartTask(BaseModel):
    id_user: int
    name_category: str
class ShortUrlCreate(BaseModel):
    original_url: str
    custom_code: Optional[str] = None
    expires_days: Optional[int] = None

class ShortUrlResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    created_at: datetime
    expires_at: Optional[datetime]
    clicks: int