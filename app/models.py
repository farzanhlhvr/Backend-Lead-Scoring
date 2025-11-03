from pydantic import BaseModel
from typing import List, Optional

class OfferIn(BaseModel):
    name: str
    value_props: List[str]
    ideal_use_cases: List[str]

class LeadOut(BaseModel):
    name: str
    role: str
    company: str
    industry: str
    location: str
    linkedin_bio: Optional[str] = None
    intent: Optional[str] = None
    score: Optional[int] = 0
    reasoning: Optional[str] = None
