from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)                    # developer's name (used as sender + section heading)
    team_name = Column(String, default="Innu Team")           # used in subject + sign-off
    email_to = Column(String, nullable=False)                 # PM ka email
    recipient_name = Column(String, nullable=False)           # e.g. "Danish" — used in "Hi {{recipient_name}}"
    github_username = Column(String, nullable=False)
    github_token = Column(String, nullable=False)
    repos = Column(JSON, default=list)                        # ["org/repo1", "org/repo2"]
    schedule_hour = Column(Integer, default=18)
    schedule_minute = Column(Integer, default=0)
    timezone = Column(String, default="Asia/Karachi")
    tone = Column(String, default="professional")              # professional / casual / concise
    default_start_time = Column(String, default="8:00 PM")     # editable, shown as-is in email
    default_end_time = Column(String, default="12:00 AM")      # editable, shown as-is in email
    default_total_hours = Column(String, default="4 Hours")    # editable
    active = Column(String, default="true")
    created_at = Column(DateTime, default=datetime.utcnow)

    reports = relationship("Report", back_populates="user")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)
    summary_text = Column(Text)
    commit_count = Column(Integer, default=0)
    repos_touched = Column(JSON, default=list)
    sent_successfully = Column(String, default="false")

    user = relationship("User", back_populates="reports")