from datetime import datetime
import json
from uuid import UUID
from fastapi.testclient import TestClient
from config import *

from main import app

client = TestClient(app)

ids = {
    "user_id": "",
    "master_id": "",
    "owner_id": "",
    "admin_id": "",
    "master_id2": ""
}

tokens = {
    "client": "",
    "master": "",
    "owner": "",
    "admin": ""
}


def test_get_info():
    response = client.get("/info")
    assert response.status_code == 200
    assert response.json() == {
        "name": NAME,
        "opening_time": OPEN_TIME,
        "close_time": CLOSE_TIME,
        "destination": DESTINATION,
        "phone_number": PHONE_NUMBER
    }


def test_get_queue_all_unauthorized():
    response = client.get("/queue/all")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Unauthorized"
    }


def test_post_register_as_client():
    response = client.post("/auth/register", json={
        "email": "client@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "role": "client"
    })

    assert response.status_code == 201
    ids['user_id'] = response.json()['id']


def test_post_register_as_master():
    response = client.post("/auth/register", json={
        "email": "master@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "role": "master"
    })

    assert response.status_code == 201
    ids['master_id'] = response.json()['id']


def test_post_register_as_admin():
    response = client.post("/auth/register", json={
        "email": "admin@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "role": "admin"
    })

    assert response.status_code == 201
    ids['master_id'] = response.json()['id']


def test_post_register_as_owner():
    response = client.post("/auth/register", json={
        "email": "owner@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "role": "owner"
    })

    assert response.status_code == 201
    ids['owner_id'] = response.json()['id']


def test_post_login_as_master():
    response = client.post("/auth/jwt/login", data={
        "username": "master@example.com",
        "password": "string"
    })

    assert response.status_code == 200
    tokens['master'] = response.json()['access_token']
    return response.json()['access_token']


def test_post_login_as_client():
    response = client.post("/auth/jwt/login", data={
        "username": "client@example.com",
        "password": "string"
    })

    assert response.status_code == 200
    tokens["client"] = response.json()['access_token']
    return response.json()['access_token']


def test_post_login_as_owner():
    response = client.post("/auth/jwt/login", data={
        "username": "owner@example.com",
        "password": "string"
    })

    assert response.status_code == 200
    tokens['owner'] = response.json()['access_token']
    return response.json()['access_token']


def test_post_login_as_admin():
    response = client.post("/auth/jwt/login", data={
        "username": "admin@example.com",
        "password": "string"
    })

    assert response.status_code == 200
    tokens['admin'] = response.json()['access_token']
    return response.json()['access_token']


def test_post_register_as_master_to_db():
    response = client.post("/master/register_as_master",
                           headers={"Authorization": f"Bearer {tokens['master']}"})

    assert response.status_code == 200
    assert response.json()["rating"] == 0
    assert response.json()["rate_count"] == 0
    ids["master_id2"] = response.json()["master_id"]


def test_post_book_to_master():
    json = {
        "master_id": ids["master_id2"],
        "starts_at": datetime.strftime(datetime.now(), format="%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'
    }

    response = client.post(
        "/queue/book",
        headers={
            "Authorization": f"Bearer {tokens['client']}"
        },
        json=json
    )
    assert response.status_code == 200


def test_post_book_to_master_busy():
    json = {
        "master_id": ids["master_id2"],
        "starts_at": datetime.strftime(datetime.now(), format="%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'
    }

    response = client.post(
        "/queue/book",
        headers={
            "Authorization": f"Bearer {tokens['client']}"
        },
        json=json
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Master is busy"
    }


def test_get_all_queue_for_master():
    response = client.get(
        f"/queue/{ids['master_id2']}",
        headers={
            "Authorization": f"Bearer {tokens['admin']}"
        }
    )
    assert response.status_code == 200


def test_put_mark_as_started():

    json = {
        "id": 1,
        "is_started": True,
        "started_at": datetime.strftime(datetime.now(), format="%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'
    }
    response = client.put(
        f"/queue/mark_as_started",
        headers={
            "Authorization": f"Bearer {tokens['admin']}"
        },
        json=json
    )

    assert response.status_code == 200
    assert response.json()['is_started'] == True


def test_put_mark_as_ended():

    json = {
        "id": 1,
        "ended_at": datetime.strftime(datetime.now(), format="%Y-%m-%dT%H:%M:%S.%f")[:-3]+'Z'
    }
    response = client.put(
        f"/queue/mark_as_ended",
        headers={
            "Authorization": f"Bearer {tokens['admin']}"
        },
        json=json
    )

    assert response.status_code == 200
