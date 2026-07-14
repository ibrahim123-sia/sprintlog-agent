from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    name: str
    email_to: str
    github_username:	str
    github_token:	str
    repos:	List[str]
    schedule_hour:	int	=	18
    schedule_minute:	int	=	0
    timezone:	str	=	"Asia/Karachi"
    tone:	str	=	"professional"

class	UserUpdate(BaseModel):
    repos:	Optional[List[str]]	=	None
    schedule_hour:	Optional[int]	=	None
    schedule_minute:	Optional[int]	=	None
    tone:	Optional[str]	=	None
    email_to:	Optional[str]	=	None