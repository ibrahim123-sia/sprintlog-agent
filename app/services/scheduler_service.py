import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.database import SessionLocal
from app.models import User, Report
from app.agents.graph import build_graph
from app.services.github_service import collect_daily_activity
from app.services.email_service import render_email, send_email
from datetime import datetime

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()
report_graph = build_graph()


def run_report_for_user(user_id: int) -> dict:
    """The actual job that runs for a single user at their scheduled time.

    Returns a status dict instead of raising, so a bad Gemini/GitHub/SMTP
    call for one user can't silently kill the scheduler job or crash the
    manual-trigger endpoint — the failure is logged and recorded as a
    Report row instead of just vanishing.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user or user.active != "true":
            return {"status": "skipped", "reason": "user not found or inactive"}

        try:
            activity = collect_daily_activity(user.repos, user.github_username, user.github_token)
        except Exception:
            logger.exception("EOD report failed for user_id=%s while collecting GitHub activity", user_id)
            db.add(Report(
                user_id=user.id,
                summary_text="Report generation failed while collecting GitHub activity — see server logs.",
                sent_successfully="false"
            ))
            db.commit()
            return {"status": "error"}

        if activity["total_commits"] == 0:
            return {"status": "skipped", "reason": "no commits today"}

        try:
            result = report_graph.invoke({"activity": activity, "tone": user.tone})
            summary = result["final_summary"]  # bullet points only — Completed Tasks section

            subject, body = render_email(
                team_name=user.team_name,
                recipient_name=user.recipient_name,
                date="{d.day}-{d.month}-{d.year}".format(d=datetime.now()),
                developer_name=user.name,
                completed_tasks=summary,
                start_time=user.default_start_time,
                end_time=user.default_end_time,
                total_hours=user.default_total_hours
            )

            send_email(user.email_to, subject, body)
        except Exception:
            logger.exception("EOD report failed for user_id=%s", user_id)
            db.add(Report(
                user_id=user.id,
                summary_text="Report generation/send failed — see server logs.",
                commit_count=activity["total_commits"],
                repos_touched=list(activity["repos"].keys()),
                sent_successfully="false"
            ))
            db.commit()
            return {"status": "error"}

        db.add(Report(
            user_id=user.id,
            summary_text=summary,
            commit_count=activity["total_commits"],
            repos_touched=list(activity["repos"].keys()),
            sent_successfully="true"
        ))
        db.commit()
        return {"status": "sent"}
    finally:
        db.close()


def schedule_user(user: User):
    """Adds or updates a cron job for a specific user."""
    job_id = f"eod_user_{user.id}"
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    scheduler.add_job(
        run_report_for_user,
        trigger=CronTrigger(hour=user.schedule_hour, minute=user.schedule_minute, timezone=user.timezone),
        args=[user.id],
        id=job_id,
        replace_existing=True
    )


def load_all_user_schedules():
    """Call this once on startup to schedule every active user."""
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.active == "true").all()
        for user in users:
            schedule_user(user)
    finally:
        db.close()