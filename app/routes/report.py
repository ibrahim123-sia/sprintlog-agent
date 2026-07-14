from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Report
from app.services.scheduler_service import run_report_for_user

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/trigger/{user_id}")
def trigger_now(user_id: int, db: Session = Depends(get_db)):
    """Manually trigger a report right now, useful for testing."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    run_report_for_user(user_id)
    return {"status": "triggered"}


@router.get("/history/{user_id}")
def get_history(user_id: int, db: Session = Depends(get_db)):
    return db.query(Report).filter(Report.user_id == user_id).order_by(Report.date.desc()).all()