from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    password: str
    mobile: Optional[str] = None
    re_type_password: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None