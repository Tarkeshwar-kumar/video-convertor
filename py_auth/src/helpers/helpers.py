from pydantic import BaseModel, Field
from typing import Optional

class UserRequest(BaseModel):
    id: Optional[str]
    first_name: str
    last_name: str
    email: str
    age: int = Field(gt=0, lt=100)
    password: str
    user_type: str
    