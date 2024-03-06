from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import time


class AgencySchema(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    fax_number: Optional[int] = None
    email: Optional[str] = None
