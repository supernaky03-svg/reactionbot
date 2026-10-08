# Thinking Auto Reaction Bot

Async Telegram control-panel foundation based on the supplied project specification.

## Included
- Telegram Bot API control panel
- Admin/user identity and permission model
- Per-user settings and channel isolation
- PostgreSQL/Neon-compatible SQLAlchemy schema
- Encrypted bot-token storage helpers
- Idempotent database constraints
- Health endpoint
- Scheduler foundation
- Telethon Userbot client foundation
- Render configuration
- Dockerfile

## Run locally

1. Copy `.env.example` to `.env`.
2. Fill in Telegram Bot token, admin ID, Neon `DATABASE_URL`, MTProto credentials and encryption key.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run:
   `python -m app.main`

For Render, deploy the health service and configure secrets in the Render dashboard.

## Important Telegram limitation
Reaction behavior depends on the current Telegram Bot API, bot permissions, target channel configuration, and supported reaction types. The worker must only report success after Telegram confirms the API request. This project intentionally does not implement API bypasses or fake success reporting.

## Production hardening
- Put the bot poller, Userbot monitor, worker, and health endpoint into separate Render services for reliable scaling.
- Use a persistent Telethon session secret rather than local filesystem state.
- Add migrations (Alembic) before schema changes.
- Implement the Userbot event handler and the Bot API reaction worker against the current Telegram API behavior.
- Add structured logging, metrics, retry/backoff policies, and integration tests.
