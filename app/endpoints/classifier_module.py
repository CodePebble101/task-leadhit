import json
import logging
import redis
from typing import Annotated

from fastapi import APIRouter, HTTPException, Body
from starlette.responses import JSONResponse
from starlette.requests import Request

from app.models.validation.classifier import ClassifierResponse, TemplateClassifier
from app.scripts.classification import get_all_data_from_mongo, find_form
from app.config.config import RedisSettings

classifier_router = APIRouter(
    prefix='',
    tags=["Forms"],
)

redis_client = redis.StrictRedis(host=RedisSettings.REDIS_HOST, port=RedisSettings.REDIS_PORT, db=0)

example_data = {
    "data": {
        "user_name": "Dmitriy",
        "birthday": "29.12.2003",
        "gift": "HTTP response with status code 418",
        "user_email": "ShaburovDA.work@yandex.ru",
        "user_phone": "+79673132702",
        "user_password": "qwerty",
        "register_date": "14.11.2023"
    }
}


@classifier_router.post(path='/get_form',
                        summary='Получение имени шаблона при его наличии',
                        description="Данный метод вернет название подходящего шаблона, если таковой будет найден. "
                                    " В ином случае полученные в запросе поля вернутся с присвоенными типами данных вместо значений",
                        response_model=ClassifierResponse)
async def get_validated_data(data: Annotated[
    TemplateClassifier,
    Body(
        examples=[
            example_data
        ],
    ),
], request: Request):
    try:
        cache_key = str(data)
        cached_data = redis_client.get(cache_key)
        if cached_data is not None:
            # берем интересующие данные из кеша
            logging.debug('Берем данные из кеша')
            return JSONResponse(status_code=200,
                                content={
                                    "status": "Success",
                                    "data": json.loads(cached_data.decode('utf-8')),
                                    "details": None
                                }
                                )
        else:
            # Если в кеше пусто, лезем в бд
            logging.debug('Берем данные из бд')
            all_forms = await get_all_data_from_mongo(request)
            finded_form = await find_form(input_data=data, mongo_data=all_forms)
            response_data = data if not finded_form else finded_form
            redis_client.setex(cache_key, 60, json.dumps(response_data))

            return JSONResponse(status_code=200,
                                content={
                                    "status": "Success",
                                    "data": response_data,
                                    "details": None
                                }
                                )
    except Exception as er:
        logging.error(er)
        raise HTTPException(status_code=500, detail={
            "status": "Error",
            "data": None,
            "details": None
        })
