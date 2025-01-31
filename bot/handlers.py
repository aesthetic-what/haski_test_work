from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy import select, insert, update
from data.database import Sessionlocal
from data.models import Users
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv('.env')
config = os.environ
API_URL = config['API_URL']
LOGIN_URL = config['LOGIN_URL']
TOKEN = config['TELEGRAM_TOKEN']
IMEI_TOKEN = config['IMEI_TOKEN']

class IMEI_state(StatesGroup):
    imei=State()
    token=State()

bot = Bot(token=TOKEN)

async def is_allowed_user(user_id: int):
    db = Sessionlocal()
    try:
        return db.query(Users).filter(Users.id == user_id).first() is not None
    finally:
        db.close()


def check_imei_(imei: int):
    url = 'https://api.imeicheck.net/v1/checks'

    token = IMEI_TOKEN

    # Add necessary headers
    headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json'
    }

    # Add body
    body =  json.dumps({
    "deviceId": f'{imei}',
    "serviceId": 12
    })

    # Execute request
    response = requests.post(url, headers=headers, data=body)
    data = response.json()
    result = f"🔍 IMEI: {imei}\n📄 Результат: {data['status']}"
    # print(data)
    print(result)
    # print(response.text)
    # print(response.json())
    return result
    
router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    keyboard = InlineKeyboardBuilder([[
        InlineKeyboardButton(text='авторизоваться', callback_data='auth')
    ]])
    if not await is_allowed_user(message.from_user.id):
        await message.answer("❌ У вас нет доступа к боту!", reply_markup=keyboard.as_markup())
        return
    await message.answer("👋 Отправьте мне IMEI для проверки.")
    await state.set_state(IMEI_state.imei)

@router.message(Command('test_func'))
async def test_func(message: Message, state: FSMContext):
    await message.answer('Введите имеи номер:')
    await state.set_state(IMEI_state.imei)
    
@router.callback_query(F.data == 'auth')
async def imei_(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите токен:')
    await state.set_state(IMEI_state.token)
    
@router.message(F.text, IMEI_state.token)
async def confirm_token(message: Message, state: FSMContext):
    token = message.text.strip()
    if not len(token) not in (14, 15):
        await message.answer("⚠️ Введите корректный токен (14-15 цифр).")
        return
    
    with Sessionlocal() as session:
        session.execute(insert(Users).values(id=message.chat.id,
                                            username=message.from_user.first_name,
                                            token=token,
                                            white_list=True))
        session.commit()
    await message.answer('Токен был успешно добавлен')

@router.message(F.text == 'check_imei')
async def check_imei(message: Message, state: FSMContext):
    if not is_allowed_user(message.from_user.id):
        await message.answer("❌ У вас нет доступа к боту!")
        return

    data = await state.get_data()
    imei = data["imei"].strip()
    
    if not imei.isdigit() or len(imei) not in (14, 15):
        await message.answer("⚠️ Введите корректный IMEI (14-15 цифр).")
        return

    # Запрос к FastAPI
    response = requests.post(API_URL, json={"imei": imei, "token": IMEI_TOKEN})

    if response.status_code == 200:
        data = response.json()
        await message.answer(f"🔍 IMEI: {imei}\n📄 Результат: {data['result']}")
    else:
        await message.answer("⚠️ Ошибка при проверке IMEI.")
        
# @router.callback_query