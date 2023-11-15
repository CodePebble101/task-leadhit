import logging

import requests
from fastapi.testclient import TestClient
from app.main import app
from app.config.config import DefaultServerSettings

mongo_data = [
    {
        "name": "Birthday form",
        "user_name": "text",
        "birthday": "date"
    },
    {
        "name": "Birthday form with gift",
        "user_name": "text",
        "birthday": "date",
        "gift": "text"
    },
    {
        "name": "Meeting with friend",
        "friend_phone": "phone",
        "meeting_date": "date",
        "meeting_place": "text"
    },
    {
        "name": "User register",
        "user_email": "email",
        "user_phone": "phone",
        "user_password": "text",
        "register_date": "date"
    }]

client = TestClient(app)

base_url = f"http://back:{DefaultServerSettings.APP_PORT}/test_leadhit/api/v1"


def test_correct_classification_without_excess_data():
    response = requests.post(base_url + "/get_form", json={
        "data": {
            "user_email": "ShaburovDA.work@yandex.ru",
            "user_phone": "+79673132702",
            "user_password": "qwerty",
            "register_date": "29.12.2003"
        }
    })

    assert response.status_code == 200
    logging.error(response.json())

    assert response.json() == {
        "status": "Success",
        "data": "User register",
        "details": None
    }


def test_correct_classification_with_excess_data():
    response = requests.post(base_url + "/get_form", json={
        "data": {
            "user_email": "ShaburovDA.work@yandex.ru",
            "user_phone": "+79673132702",
            "user_password": "qwerty",
            "register_date": "29.12.2003",
            "taxi_car": "Lada",
            "IObound": "100500%"
        }
    })

    assert response.status_code == 200
    logging.error(response.json())

    assert response.json() == {
        "status": "Success",
        "data": "User register",
        "details": None
    }


def test_validation():
    response = requests.post(base_url + "/get_form", json={
        "data": {
            "user_email": "ShaburovDA.work@yandex.ru",
            "user_phone": 79673132702,
        }
    })
    assert response.status_code == 422


def test_classification():
    response = requests.post(base_url + "/test/classification", json={
        "data": {
            "user_number": "+79673132702",
            "user_mail": "ShaburovDA.work@yandex.ru",
            "birthday": "29.12.2003",
            "city": "Moscow"
        }
    })
    assert response.status_code == 200
    assert response.json() == {
        "status": "Success",
        "data": {
            "user_number": "phone",
            "user_mail": "email",
            "birthday": "date",
            "city": "text"
        },
        "details": None
    }


def test_right_choice():
    response = requests.post(base_url + "/get_form", json={
        "data": {
            "user_name": "text",
            "gift": "text",
            "user_number": "+79673132702",
            "user_mail": "ShaburovDA.work@yandex.ru",
            "birthday": "29.12.2003",
            "city": "Moscow"
        }
    })
    assert response.status_code == 200
    assert response.json() == {
        "status": "Success",
        "data": "Birthday form with gift",
        "details": None
    }


def test_empty_request():
    response = requests.post(base_url + "/get_form", json={

    })
    assert response.status_code == 422


def test_extraneous_data():
    response = requests.post(base_url + "/get_form", json={
        "data": {
            "purchaser_phone": "+78005553535",
            "purchaser_wish": "The Best site in The World",
        }
    })
    assert response.status_code == 200
    assert response.json() == {
        "status": "Success",
        "data": {
            "purchaser_phone": "phone",
            "purchaser_wish": "text",
        },
        "details": None
    }


if __name__ == '__main__':
    test_correct_classification_without_excess_data()
