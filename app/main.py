from fastapi import FastAPI
from app.database import engine, Base
from app.routes import users,reports
from app.services.scheduler_service import scheduler,load_all_user_schedules

Base.metadata.create_all(bind=engine)

app=FastAPI(title="sprintlog-agent")

app.include_router(users.router)
app.include_router(reports.router)

@app.on_event("startup")
def startup_event():
    scheduler.start()
    load_all_user_schedules()
   
@app.on_event("shutdown")
def	shutdown():
    scheduler.shutdown()

@app.get("/")
def health_check():
    return {"status": "ok"}