import logging
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "6428280685:AAGbtirZz3zlaw9LouJVkaNvln-gOh85blI"
GROUP_ID = -1002394380486  # ID вашей группы

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

# Маппинг: message_id в группе -> user_id
GROUP_MSG_MAP = {}

def format_user_info(user: types.User) -> str:
    username = f"@{user.username}" if user.username else "(нет username)"
    return f"ID: <code>{user.id}</code>\nUsername: {username}\nИмя: {user.full_name}"

@dp.message_handler(commands=["start"], chat_type=types.ChatType.PRIVATE)
async def send_welcome(message: types.Message):
    await message.reply("👋 Привет! Отправь сюда свою предложку (текст, фото, видео).")

# Приём предложки и пересылка в группу
@dp.message_handler(content_types=types.ContentTypes.ANY, chat_type=types.ChatType.PRIVATE)
async def handle_suggestion(message: types.Message):
    user_info = format_user_info(message.from_user)
    header = f"📩 Новая предложка\n{user_info}"

    # Заголовок в группу
    header_msg = await bot.send_message(GROUP_ID, header)

    # Копия контента в группу как ответ на заголовок
    copied = await message.copy_to(GROUP_ID, reply_to_message_id=header_msg.message_id)

    # Сохраняем соответствие: ID сообщения в группе -> ID пользователя
    GROUP_MSG_MAP[copied.message_id] = message.from_user.id

    # Подтверждение пользователю
    await message.reply("✅ Ваша предложка отправлена в группу на рассмотрение.")

# Ответ из группы → пользователю
@dp.message_handler(content_types=types.ContentTypes.TEXT,
                    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def reply_from_group(message: types.Message):
    if message.reply_to_message:
        replied_id = message.reply_to_message.message_id
        user_id = GROUP_MSG_MAP.get(replied_id)

        if user_id:
            await bot.send_message(user_id, f"💬 Ответ из группы:\n{message.text}")
        else:
            await message.reply("⚠️ Не найдено соответствие пользователю. Ответьте именно на скопированное сообщение предложки.")

if __name__ == "__main__":
    print("Bot started...")
    executor.start_polling(dp, skip_updates=True)

