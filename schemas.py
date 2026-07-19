from datetime import date
from pydantic import BaseModel, ConfigDict
from enums import Difficulty

class ProblemCreate(BaseModel):
    title : str
    difficulty: Difficulty
    category: str
    subcategory: str | None=None
    last_ac_date: date

class ProblemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id : int
    title : str
    difficulty: Difficulty
    category: str
    subcategory: str | None=None
    last_ac_date: date   

class ProblemACUpdate(BaseModel):
    last_ac_date: date