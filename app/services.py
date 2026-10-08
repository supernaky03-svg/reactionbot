import math, random, re
from datetime import datetime, timedelta
from urllib.parse import urlparse
from sqlalchemy import select
from .models import User, UserPermission, UserSetting, Channel, BotToken, Job, ReactionTask

PERMISSIONS = ["add_channel","remove_channel","link_reaction","channels","settings","help","contact_admin",
               "add_bot","remove_bot","users","add_user","ban_user","permission"]

def parse_public_link(value: str):
    p = urlparse(value.strip())
    if p.scheme not in ("http","https") or p.netloc not in ("t.me","telegram.me"):
        raise ValueError("Invalid Telegram link")
    parts = [x for x in p.path.split("/") if x]
    if len(parts) < 1 or parts[0].startswith("+") or parts[0] == "joinchat":
        raise ValueError("Public Telegram link required")
    username = parts[0].lstrip("@")
    message_id = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
    return username, message_id

async def ensure_user(session, tg_user, admin_id):
    q = await session.execute(select(User).where(User.telegram_id == tg_user.id))
    user = q.scalar_one_or_none()
    if not user:
        user = User(telegram_id=tg_user.id, username=tg_user.username, display_name=tg_user.full_name)
        session.add(user); await session.flush()
        admin = tg_user.id == admin_id
        perm = UserPermission(user_id=user.id, **{p: admin for p in PERMISSIONS})
        setting = UserSetting(user_id=user.id)
        session.add_all([perm, setting])
        await session.commit()
    return user

async def is_allowed(session, tg_id, admin_id):
    if tg_id == admin_id: return True
    q = await session.execute(select(User).where(User.telegram_id == tg_id))
    u = q.scalar_one_or_none()
    return bool(u and u.status == "active")

async def has_permission(session, tg_id, name, admin_id):
    if tg_id == admin_id: return True
    q = await session.execute(select(User, UserPermission).join(UserPermission, UserPermission.user_id == User.id)
                              .where(User.telegram_id == tg_id))
    row = q.first()
    return bool(row and row[0].status == "active" and getattr(row[1], name, False))

def target_range(active_count: int, rate: int):
    minimum = math.ceil(active_count * rate / 100)
    return minimum, active_count

def make_schedule(count, start, seconds):
    if count <= 0: return []
    if seconds <= 0: return [start] * count
    offsets = sorted(random.randint(0, seconds) for _ in range(count))
    return [start + timedelta(seconds=x) for x in offsets]
