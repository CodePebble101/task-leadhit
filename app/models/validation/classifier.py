import re
from typing import Dict
from pydantic import model_validator, BaseModel

from app.models.validation.defaults import BasicResponse


# наследуемся от созданного дефолтного ответа и добавляем в него нужные данные
class ClassifierResponse(BasicResponse):
    data: Dict[str, str]


# после проверки на то, что ключи и значения имеют строковый тип данных (исходя из ТЗ) классифицируем поля значений
class TemplateClassifier(BaseModel):
    data: Dict[str, str]

    @model_validator(mode="after")
    @classmethod
    def validate_data(cls, values):
        allowed_groups = {
            "date": re.compile(
                r"((0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d)|(20\d\d-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01]))"),
            "phone": re.compile(r"^((\+7)+([0-9]){10})$"),
            "email": re.compile(r"^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$")
        }

        classified_data = {}
        for key, value in values.data.items():
            matched_group = None
            for group, pattern in allowed_groups.items():
                if pattern.match(value):
                    matched_group = group
                    break

            classified_data[key] = matched_group if matched_group else 'text'

        return classified_data
