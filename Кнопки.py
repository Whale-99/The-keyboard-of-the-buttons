from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

# Токен бота
api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage= MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton( text = 'Информация')
button2 = KeyboardButton( text = 'Начать')
kb.add(button)
kb.add(button2)
@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer ('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text = 'Информация')
async def inform(message):
    await message.answer("Нажми 'Начать' для расчета калорий.")

@dp.message_handler(text = 'Начать')
async def set_age(message: types.Message, state: FSMContext):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        await state.update_data(age=age)  # Сохраняем возраст
        await message.answer("Введите свой рост:")
        await UserState.growth.set()
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение для возраста.")

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    try:
        growth = int(message.text)
        await state.update_data(growth=growth)  # Сохраняем рост
        await message.answer("Введите свой вес:")
        await UserState.weight.set()
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение для роста.")

@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    try:
        weight = int(message.text)
        await state.update_data(weight=weight)  # Сохраняем вес

        # Получаем все данные
        data = await state.get_data()
        age = data['age']
        growth = data['growth']
        weight = data['weight']

        # Формула Миффлина-Сан Жеора для расчета калорийности
        calories = 10 * weight + 6.25 * growth - 5 * age + 5

        # Отправляем результат пользователю
        await message.answer(f"Ваша дневная норма калорий: {calories:.2f} ккал.")

        # Завершаем машину состояний
        await state.finish()
    except ValueError:
        await message.answer("Пожалуйста, введите числовое значение для веса.")


# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
