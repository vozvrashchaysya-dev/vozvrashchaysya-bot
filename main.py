import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.executor import start_webhook
from aiogram.dispatcher.filters import Text

API_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_PATH = f"/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", default=3000))

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Quiz(StatesGroup):
    q1 = State()
    q2 = State()
    result = State()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton("О концепте"))
kb.add(KeyboardButton("Пройти мини-тест"))
kb.add(KeyboardButton("Структура пакета"))
kb.add(KeyboardButton("Купить доступ"))
kb.add(KeyboardButton("FAQ"))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
     await message.answer("Концепт: ВОЗВРАЩАЙСЯ!\n 
Ты здесь, чтобы захотеть вернуться.\n
Выбери:", reply_markup=kb)

@dp.message_handler(Text(equals="О концепте"))
async def about(message: types.Message):
    await message.answer("ВОЗВРАЩАЙСЯ — не маркетинг. Это след, который хочется найти снова.")

@dp.message_handler(Text(equals="Пройти мини-тест"))
async def quiz_start(message: types.Message):
    await Quiz.q1.set()
    await message.answer("1/2: Что ты хочешь оставить после себя?
— Свободу
— Память
— Желание вернуться")

@dp.message_handler(state=Quiz.q1)
async def quiz_q1(message: types.Message, state: FSMContext):
    await Quiz.q2.set()
    await message.answer("2/2: Когда ты хочешь вернуться?
— Когда тебя не держат
— Когда остался след
— Когда звучал собой")

@dp.message_handler(state=Quiz.q2)
async def quiz_result(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Тебе близок концепт «Возвращайся!»
Хочешь материалы — нажми «Купить доступ».")

@dp.message_handler(Text(equals="Структура пакета"))
async def structure(message: types.Message):
    await message.answer("Пакет включает PDF-гайд, чек-листы, шаблоны, инструкции.")

@dp.message_handler(Text(equals="Купить доступ"))
async def buy(message: types.Message):
    await message.answer("Это прототип. Здесь будет кнопка WalletPay и авто-выдача.")

@dp.message_handler(Text(equals="FAQ"))
async def faq(message: types.Message):
    await message.answer("FAQ: оплата через Telegram, материалы приходят мгновенно, всё автономно.")

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
