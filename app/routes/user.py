from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schema import UserCreate, UserUpdate
from app.services.scheduler_service import schedule_user


router=APIRouter(prefix="/users", tags=["users"])

@router.post('/')
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = User(**payload.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    schedule_user(user)  # Schedule the user's report job
    return user

@router.patch('/{user_id}')
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    schedule_user(user)  # Reschedule the user's report job
    return user

@router.get('/{user_id}')
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user