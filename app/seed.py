"""
Seed script — creates the initial user for Sprintlog.
Run this once after setting up the database, from the repo root: python -m app.seed
"""
from app.config import settings
from app.database import SessionLocal, Base, engine
from app.models import User
from app.services.scheduler_service import schedule_user

# Make sure tables exist
Base.metadata.create_all(bind=engine)

def seed_user():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.github_username == "ibrahim123-sia").first()
        if existing:
            print("User already exists, skipping seed.")
            return existing

        user = User(
           name="Syed Ibrahim",
            email_to="aryanaj2255@gmail.com",
            recipient_name="Aryan",
            github_username=settings.github_username,
            github_token=settings.github_token,
            repos=["ibrahim123-sia/sprintlog-agent"], # apne repos daal do
            schedule_hour=18,
            schedule_minute=0,
            timezone="Asia/Karachi",
            tone="professional"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"User created with id: {user.id}")
        return user
    finally:
        db.close()

if __name__ == "__main__":
    seed_user()