# Sprintlog

Autonomous multi-agent AI system that eliminates manual EOD reporting. Analyzes daily GitHub commits and diffs, reasons about code changes via a LangGraph pipeline (context, prioritization, and writer agents), then drafts and sends personalized end-of-day progress emails — powered by LangChain, Gemini, FastAPI, and Neon PostgreSQL.

## Why

Manually reviewing GitHub commits every day and writing an EOD report to your PM is repetitive and easy to forget. Sprintlog automates the entire flow — from reading raw commits to sending a ready-to-read email — with zero manual writing required.

## How it works

1. **Collector Agent** — pulls today's commits and diffs from GitHub
2. **Context Agent** — reads the diffs (not just commit messages) to understand what actually changed
3. **Prioritizer Agent** — separates high-impact work from minor/maintenance changes
4. **Writer Agent** — drafts the final EOD email body in the user's chosen tone
5. **Sender Agent** — emails the report and logs it to the database

Each user has their own configurable GitHub repos, schedule time, and tone — the system supports multiple users, not just a single hardcoded setup.

## Tech stack

- **Backend:** FastAPI (Python)
- **Agent orchestration:** LangGraph
- **Prompting:** LangChain (`ChatPromptTemplate`)
- **LLM:** Google Gemini (via `langchain-google-genai`)
- **Database:** PostgreSQL via Neon (serverless, free tier)
- **Scheduling:** APScheduler — dynamic, per-user cron jobs
- **Email:** SMTP
- **Templates:** Jinja2

## Project structure

```
sprintlog-agent/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schema.py
│   ├── seed.py
│   ├── services/
│   │   ├── github_service.py
│   │   ├── email_service.py
│   │   └── scheduler_service.py
│   ├── agents/
│   │   ├── graph.py
│   │   ├── context_agent.py
│   │   ├── prioritizer_agent.py
│   │   └── writer_agent.py
│   ├── templates/
│   │   └── eod_email.txt
│   ├── routes/
│   │   ├── user.py
│   │   └── report.py
│   ├── requirements.txt
│   ├── .env.example
│   └── .env            (create this, not committed)
└── README.md
```

## Setup

All commands below are run from the repo root (`sprintlog-agent/`), not from inside `app/`.

1. Clone the repo and install dependencies:
   ```bash
   pip install -r app/requirements.txt
   ```

2. Copy `app/.env.example` to `app/.env` and fill in your values:
   ```
   DATABASE_URL=your-neon-connection-string
   GEMINI_API_KEY=your-gemini-api-key
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email
   SMTP_PASSWORD=your-app-password
   SECRET_KEY=any-random-string
   GITHUB_TOKEN=ghp_xxxxx
   GITHUB_USERNAME=your-github-username
   ```
   (`app/.env` is used regardless of your current directory — `config.py` resolves it relative to its own location.)

3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   This also creates the database tables on first run.

4. Create a user — either via the seed script (edit the placeholder values in `app/seed.py` first):
   ```bash
   python -m app.seed
   ```
   or via the API directly (`recipient_name` is required — it's who the email greeting is addressed to):
   ```bash
   curl -X POST http://localhost:8000/users/ \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Your Name",
       "email_to": "pm@company.com",
       "recipient_name": "PM Name",
       "github_username": "your-github-username",
       "github_token": "ghp_xxxxx",
       "repos": ["your-org/your-repo"],
       "schedule_hour": 18,
       "schedule_minute": 0,
       "tone": "professional"
     }'
   ```

5. Trigger a report manually (for testing — only sends an email if the configured repo has commits by that GitHub user today):
   ```bash
   curl -X POST http://localhost:8000/reports/trigger/1
   ```

## Roadmap

- [ ] Weekly summary agent (aggregates past 7 days)
- [ ] Slack/Discord delivery option
- [ ] Simple settings UI
- [ ] Better error handling and GitHub API rate-limit handling

## License

MIT
