from fastapi import FastAPI
from routers.auth import router

app = FastAPI()

app.include_router(router)

@app.get('/')
async def start():
    return {'hello': 'world'}
