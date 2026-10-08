from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from sqlalchemy import select
from .config import settings
from .db import SessionLocal
from .models import User, Channel, UserSetting
from .services import ensure_user, is_allowed, has_permission

bot = Bot(settings.bot_token)
dp = Dispatcher()

def menu(admin=False):
    rows = [[KeyboardButton(text="Add Channel"), KeyboardButton(text="Remove Channel")],
            [KeyboardButton(text="Link Reaction"), KeyboardButton(text="Channels")],
            [KeyboardButton(text="Settings"), KeyboardButton(text="Help")],
            [KeyboardButton(text="Contact Admin")]]
    if admin:
        rows += [[KeyboardButton(text="Add User"), KeyboardButton(text="Ban User")],
                 [KeyboardButton(text="Add Bot"), KeyboardButton(text="Remove Bot")],
                 [KeyboardButton(text="Users"), KeyboardButton(text="Permission")]]
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

@dp.message(CommandStart())
async def start(m: Message):
    async with SessionLocal() as s:
        await ensure_user(s, m.from_user, settings.admin_user_id)
        if not await is_allowed(s, m.from_user.id, settings.admin_user_id):
            await m.answer("Contact @mnsm6003 to use this bot.")
            return
    await m.answer("Welcome to Thinking Auto Reaction Bot.", reply_markup=menu(m.from_user.id == settings.admin_user_id))

@dp.message()
async def all_messages(m: Message):
    async with SessionLocal() as s:
        if not await is_allowed(s, m.from_user.id, settings.admin_user_id):
            return
        text = (m.text or "").strip()
        mapping = {
            "Add Channel": "add_channel", "Remove Channel": "remove_channel",
            "Link Reaction": "link_reaction", "Channels": "channels", "Settings": "settings",
            "Help": "help", "Contact Admin": "contact_admin"
        }
        if text in mapping and not await has_permission(s, m.from_user.id, mapping[text], settings.admin_user_id):
            await m.answer("❌ You don't have permission to use this feature."); return
        if text == "Channels":
            q = await s.execute(select(Channel).join(User, Channel.owner_user_id == User.id)
                                .where(User.telegram_id == m.from_user.id))
            chans = q.scalars().all()
            await m.answer("Your Channels\n\n" + ("\n".join(f"🟢 @{c.username or c.telegram_chat_id}" for c in chans) if chans else "No channels configured."))
        elif text == "Settings":
            q = await s.execute(select(UserSetting).join(User, UserSetting.user_id == User.id).where(User.telegram_id == m.from_user.id))
            x = q.scalar_one()
            await m.answer(f"Settings\n\nReaction Rate: {x.reaction_rate}%\nDefault Delay: {x.default_delay_seconds//60} minutes\nAllowed: {' '.join(x.allowed_reactions)}")
        elif text == "Help":
            await m.answer("Add Channel — add a public channel to your monitoring list.\nLink Reaction — create a reaction job from a public post link.\nChannels — view your channels.\nSettings — configure your own rate, delay and reactions.")
        elif text == "Contact Admin":
            await m.answer("For support, contact @mnsm6003.")
        elif text in ("Add Channel","Remove Channel","Link Reaction","Add User","Ban User","Add Bot","Remove Bot","Users","Permission"):
            await m.answer("This flow is wired to the service layer; connect the Userbot/worker configuration in .env and continue with the documented production flow.")
        else:
            await m.answer("Use the menu buttons to continue.")
