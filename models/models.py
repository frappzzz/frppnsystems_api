from pydantic import BaseModel

class JsonCategory(BaseModel):
    id_user: int
    name_category: str

class JsonStartTask(BaseModel):
    id_user: int
    name_category: str