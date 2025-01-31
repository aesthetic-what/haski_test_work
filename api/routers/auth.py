from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from data.models import Users
from data.database import Sessionlocal, engine
from sqlalchemy import select, update, insert
from dotenv import load_dotenv
import os
import requests
from dotenv import load_dotenv
from api.routers.key_gen import generate_token
import hashlib
import os
import json

load_dotenv('.env')
config = os.environ
API_URL = config['API_URL']
LOGIN_URL = config['LOGIN_URL']
TOKEN = config['TELEGRAM_TOKEN']
IMEI_TOKEN = config['IMEI_TOKEN']
IMEI_URL = config['IMEI_URL']

def generate_token():
    random_bytes = os.urandom(32)
    return hashlib.sha256(random_bytes).hexdigest()

load_dotenv('.env')
config = os.environ

router = APIRouter(tags=['authtification'], prefix='/auth')

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

def check_imei(imei: int, token: str):
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
    result = {"imei": imei,
              "result": data['status']}
    # print(data)
    print(result)
    # print(response.text)
    # print(response.json())
    return result

# # Авторизация (логин)
# @router.post("/auth")
# def login(user: UserLogin, Authorize: AuthJWT = Depends()):
#     if user.username not in  or  != user.password:
#         raise HTTPException(status_code=401, detail="Неверный логин или пароль")

#     access_token = Authorize.create_access_token(subject=user.username)
#     return {"access_token": access_token}

# Эндпоинт API для проверки IMEI
@router.post("/api/check-imei")
async def check_imei_api(imei: str, token: str, db: Session = Depends(get_db)):
    api_token = db.query(Users).filter(Users.token == token).first()
    if not api_token:
        raise HTTPException(status_code=403, detail="Недействительный токен")
    return check_imei(imei, token)

# Добавление в белый список
@router.post("/whitelist/add")
async def add_to_whitelist(telegram_id: str, db: Session = Depends(get_db)):
    user = Users(id=telegram_id, white_list=True)
    db.add(user)
    db.commit()
    return {"message": "Пользователь добавлен в белый список"}

@router.get("/whitelist/check/{telegram_id}")
async def check_whitelist(telegram_id: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == telegram_id, Users.white_list == True).first()
    return {"whitelisted": bool(user),
            "token": user.token}

@router.get('/auth/{telegram_id}')
async def add_token(telegram_id: str, token: str, db: Session = Depends(get_db)):
    user = db.scalars(select(Users).where(Users.id == telegram_id)).first()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='user was not found')
    if token != user.token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='incorrect token')
    
@router.get('/generate_token/{telegram_id}')
async def token(telegram_id: int, db: Session = Depends(get_db)):
    token = generate_token()
    user = db.scalars(select(Users).where(Users.id == telegram_id)).first()
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='user was not found')
    db.execute(update(Users).values(token=token).where(Users.id == telegram_id))
    db.commit()
    return {'status_code': status.HTTP_202_ACCEPTED,
            'transaction': f'Successfuly token added to {user.username}'}