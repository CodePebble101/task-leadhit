import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Body
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.models.validation.classifier import ClassifierResponse, TemplateClassifier
from app.scripts.classification import get_all_data_from_mongo

test_router = APIRouter(
    prefix='/test',
    tags=["For tests"],
)


@test_router.post(path='/classification',
                  summary='Получение классифицированных типов данных полей',
                  response_model=ClassifierResponse)
async def get_validated_data(data: Annotated[
    TemplateClassifier,
    Body(
        examples=[
            {
                "data": {
                    "user_number": "+79673132702",
                    "user_mail": "ShaburovDA.work@yandex.ru",
                    "birthday": "29.12.2003"
                }
            }
        ],
    ),
]):
    try:
        return JSONResponse(status_code=200,
                            content={
                                "status": "Success",
                                "data": data,
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


@test_router.get(path='/all_data',
                  summary='Получение всех данных из MongoDB')
async def get_all_data(request:Request):
    try:
        all_data = await get_all_data_from_mongo(request)
        return JSONResponse(status_code=200,
                            content={
                                "status": "Success",
                                "data": all_data,
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