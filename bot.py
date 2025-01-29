import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router, types
from aiogram.types import Message
import aiohttp

router = Router()

# Роутер для команды /deepseek
@router.message(commands=['deepseek'])
async def handle_deepseek_request(message: Message):
    # Извлекаем текст после команды
    prompt = message.text.split('/deepseek', 1)[-1].strip()
    
    if not prompt:
        await message.answer("Пожалуйста, укажите запрос после команды /deepseek\nПример: /deepseek Как работает ИИ?")
        return

    try:
        # Отправляем запрос в DeepSeek API
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer YOUR_DEEPSEEK_API_KEY",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "model": "deepseek-chat"
            }

            async with session.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    answer = data['choices'][0]['message']['content']
                    await message.answer(answer)
                else:
                    await message.answer("Ошибка при обработке запроса")

    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")

# Ваш существующий эхо-хендлер
@router.message()
async def echo_message(message: Message):
    await message.answer(f"Ты написал: {message.text}")

# Вставь сюда свой токен
TOKEN = "7587958511:AAEcNhrHMcnA2jjTQdcZ7ksBJAfaeKXGRbI"

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Логирование
logging.basicConfig(level=logging.INFO)

# Команда /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я твой бот 🤖. Напиши /help, чтобы узнать, что я умею.")

# Команда /help
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Я умею отвечать на команды: \n/start - запустить бота \n/help - список команд")

# Ответ на обычные сообщения
@dp.message()
async def echo_message(message: Message):
    await message.answer(f"Ты написал: {message.text}")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())