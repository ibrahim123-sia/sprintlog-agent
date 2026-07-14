from pydantic import BaseModel
from typing import List, Optional


class UserCreate(BaseModel):
    name: str
    team_name: str = "Innu Team"
    email_to: str
    recipient_name: str
    github_username: str
    github_token: str
    repos: List[str]
    schedule_hour: int = 18
    schedule_minute: int = 0
    timezone: str = "Asia/Karachi"
    tone: str = "professional"
    default_start_time: str = "8:00 PM"
    default_end_time: str = "12:00 AM"
    default_total_hours: str = "4 Hours"


class UserUpdate(BaseModel):
    repos: Optional[List[str]] = None
    schedule_hour: Optional[int] = None
    schedule_minute: Optional[int] = None
    tone: Optional[str] = None
    email_to: Optional[str] = None
    recipient_name: Optional[str] = None
    team_name: Optional[str] = None
    default_start_time: Optional[str] = None
    default_end_time: Optional[str] = None
    default_total_hours: Optional[str] = None