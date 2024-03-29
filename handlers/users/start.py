# Bu kod t.me/uzbsobirov tomonidan yozilgan, mualliflik xuquqini saqlang!
# Faqat API ni oling kodga tegmang!

import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.main import main
from data.config import ADMINS, CHANNELS
from loader import dp, db, bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.misc.subscription import check

@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    full_name = message.from_user.full_name
    user_id = message.from_user.id
    username = message.from_user.username
    user_data = message.from_user.get_mention(f"{full_name}", as_html=True)
    

    # Foydalanuvchini bazaga qo'shamiz
    try:
        users = await db.add_user(user_id=user_id, full_name=full_name, username=username)
        # Adminga xabar beramiz
        msg = f"{user_data} bazaga qo'shildi."
        await bot.send_message(chat_id=ADMINS[0], text=msg)

    except asyncpg.exceptions.UniqueViolationError as err:
        await bot.send_message(chat_id=ADMINS[0], text=f"{user_data} bazaga oldin qo'shilgan")

    for ch in CHANNELS:
        status = await check(user_id=user_id, channel=ch)



    if status is False:
        # Majburiy obuna uchun inline button yasaymiz!
        markup = InlineKeyboardMarkup(row_width=1)
        for channel in CHANNELS:

            chat = await bot.get_chat(channel)
            invite_link = await chat.export_invite_link()
            markup.insert(InlineKeyboardButton(text=chat.title, url=invite_link))
        markup.add(InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data='check_subs'))
        await message.answer(f"<b>Assalomu aleykum {full_name}! Botimizdan to'liq foydalanishingiz uchun bizning "
                         f"kanallarimizga obuna bo'lishingiz kerak!</b>", reply_markup=markup)
    else:
        await message.answer(text=f"<b>Assalomu aleykum {full_name}! "
                                       f"Sizni botda ko'rib turganimizdan xursandmiz😊</b>", reply_markup=main)