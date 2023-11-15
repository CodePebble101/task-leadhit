import json
import logging

import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.requests import Request

from app.models.validation.classifier import TemplateClassifier


async def get_all_data_from_mongo(request):
    mongo_client: AsyncIOMotorClient = request.app.state.mongo_client['test_db']
    cursor =  mongo_client.templates.find({})
    result_data = []
    for document in await cursor.to_list(length=100):
        document["_id"] = str(document["_id"])
        result_data.append(document)
    return result_data


async def find_form(input_data: TemplateClassifier, mongo_data: list[dict]):
    exclude_fields = ["_id", "name"]
    filtered_list = []
    for obj in mongo_data:
        filtered_obj = {key: obj[key] for key in obj if key not in exclude_fields}
        if all(key in input_data and input_data[key] == filtered_obj[key] for key in filtered_obj):
            filtered_list.append(obj)
    max_correct_size = 0
    finded_name = ''
    for form in filtered_list:
        if len(form) > max_correct_size:
            max_correct_size = len(form)
            finded_name = form['name']

    return finded_name
