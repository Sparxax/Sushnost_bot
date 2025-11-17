import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "6428280685:AAGbtirZz3zlaw9LouJVkaNvln-gOh85blIТА"

# список админов (твои ID + ID других админов)
ADMINS = [5231769401]  
# если хочешь пересылку в группу, укажи ID группы (со знаком минус)
GROUP_ID = -1002394380486  

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Приветствие
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("👋 Привет! Отправь сюда свою предложку (текст, фото, видео).")

# Приём предложки
@dp.message_handler(content_types=types.ContentTypes.ANY)
async def handle_suggestion(message: types.Message):
    user_info = f"ID: {message.from_user.id}\n" \
                f"Username: @{message.from_user.username}\n" \
                f"Имя: {message.from_user.full_name}"

    # уведомление пользователю
    await message.reply("✅ Ваша предложка отправлена на рассмотрение, ожидайте.")

    # пересылка админам
    for admin_id in ADMINS:
        await bot.send_message(admin_id, f"📩 Новая предложка:\n{user_info}")
        await message.copy_to(admin_id)

    # пересылка в группу (если нужно)
    if GROUP_ID:
        await bot.send_message(GROUP_ID, f"📩 Новая предложка:\n{user_info}")
        await message.copy_to(GROUP_ID)

# Ответ пользователю через бота
@dp.message_handler(content_types=types.ContentTypes.TEXT, chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def reply_to_user(message: types.Message):
    if message.reply_to_message and message.from_user.id in ADMINS:
        if message.reply_to_message.forward_from:
            user_id = message.reply_to_message.forward_from.id
            await bot.send_message(user_id, f"💬 Ответ от админа:\n{message.text}")

# 🚀 Запуск бота
if __name__ == "__main__":
    print("Bot started...")
    executor.start_polling(dp, skip_updates=True)
