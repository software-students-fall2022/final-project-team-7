import sys
sys.path.append('.')
print(sys.path)

from app import app
from flask import Flask, render_template, session
import pytest
import pytest_flask
import pymongo
import mongomock
import os


@pytest.fixture(scope='session')
def client():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['username'] = 'test'
            session['user_id'] = '639fe8c38d2fcfefcd49fa53'
        yield client


def test_base_template(client):
    # Test login route
    url = '/'
    response = client.get(url)
    assert response.status_code == 200


def test_error_template(client):
    # Test a route that does not exist
    url = '/errornotexist'
    response = client.get(url)
    assert response.status_code == 404


def test_register_template(client):
    # Test register route
    url = '/register'
    response = client.get(url)
    assert response.status_code == 200


def test_home_template(client):
    # Test home route
    url = '/home'
    response = client.get(url)
    assert response.status_code == 200


def test_history_template(client):
    # Test history route
    url = '/history'
    response = client.get(url)
    assert response.status_code == 200


def test_history_range_template(client):
    # Test history route
    url = '/history/all'
    response = client.get(url)
    assert response.status_code == 200

    url = '/history/today'
    response = client.get(url)
    assert response.status_code == 200

    url = '/history/this_week'
    response = client.get(url)
    assert response.status_code == 200


def test_profile_template(client):
    # Test profile route
    url = '/profile'
    response = client.get(url)
    assert response.status_code == 200


def test_edit_template(client):
    # Test edit route
    url = '/edit'
    response = client.get(url)
    assert response.status_code == 200


def test_chatroom_template(client):
    # Test edit route
    url = '/chatroom'
    response = client.get(url)
    assert response.status_code == 200
