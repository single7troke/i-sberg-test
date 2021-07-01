from fastapi import FastAPI
from sqlalchemy.sql import text

from db import database, engine
from models import metadata, devices, endpoints
from random_data import create_data
from schemas import Anagram, CheckAnagramResponse, DevicesWithoutEndpoint
from anagram_checker import is_anagram
from redis import init_redis_pool

app = FastAPI()
metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    app.state.redis = await init_redis_pool()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    app.state.redis.close()
    await app.state.redis.wait_closed()
    await database.disconnect()


@app.get("/", response_model=DevicesWithoutEndpoint)
async def get_data():
    """
    Получает список всех устройств, которые не привязаны к endpoint.
    Возвращает количество, сгруппированное по типам устройств.
    """
    SQL = text('''
    select dev_type, count(dev_type) 
    from devices 
    where id not in (
        select device_id 
        from devices join  endpoints 
        on  devices.id = endpoints.device_id
        ) 
    group by dev_type order by count;''')

    data = await database.fetch_all(SQL)
    return {'devices_by_type': [dict(i) for i in list(data)]}


@app.post("/", status_code=201)
async def insert_new_data():
    """
    Добавляет в таблицу devices 10 устройств, 5 из которых привязываются к таблице endpoints
    """
    SQL = text('select * from devices order by id desc limit 5')
    insertion_data_to_devices = create_data()
    insertion_data_to_endpoints = []

    query = devices.insert().values(insertion_data_to_devices)
    await database.execute(query)
    last_five_rows = await database.fetch_all(SQL)

    for row in last_five_rows:
        insertion_data_to_endpoints.append({'device_id': row["id"],
                                            'text': f'dev_id: {row["dev_id"]},dev_type: {row["dev_type"]}'})
    query = endpoints.insert().values(insertion_data_to_endpoints)
    await database.execute(query)


@app.post("/check_anagram/", response_model=CheckAnagramResponse)
async def check_anagram(input_data: Anagram):
    """
    Проверяет являются ли строки анаграммами, если являются,
    счетчик увеличивается на 1.
    Возвращает значение проверки и значение счетчика.
    """
    first_string, second_string = input_data.first_string, input_data.second_string
    result = is_anagram(first_string, second_string)
    if result:
        await app.state.redis.incr("counter")
    count = await app.state.redis.get("counter")
    if not count:
        count = 0
    return {"is_anagram": result, "counter": count}
