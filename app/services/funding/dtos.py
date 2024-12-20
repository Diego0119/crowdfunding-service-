from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# dtos para el proyecto
class ProjectBase(BaseModel):
    name: str 
    description: str  
    goal_amount: float 
    start_date: datetime  
    end_date: datetime 
    category: str 
    rewards: str  

class ProjectCreate(BaseModel):
    name: str
    description: str
    goal_amount: float
    start_date: str
    end_date: str
    category: str
    rewards: str

class ProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    goal_amount: Optional[float]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    category: Optional[str]
    rewards: Optional[str]
    status: Optional[str]  


class ProjectOut(ProjectBase):
    id: int 
    contributions_count: int  
    current_amount: float  
    status: str  

    class Config:
        from_attributes = True  

# dtos para la contribucion
class ContributionBase(BaseModel):
    amount: float
    payment_method: str

class ContributionOut(ContributionBase):
    id: int 
    project_id: int  
    user_id: int  
    contributed_at: datetime  

    class Config:
        from_attributes = True    

class EvaluationCreate(BaseModel):
    rating: int
    comment: Optional[str] = None
