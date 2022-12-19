import sys
sys.path.append('.')
print(sys.path)

import pytest_flask
import pytest
from flask import Flask, render_template, session
from app import app


@pytest.fixture()
def client():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session['username'] = 'bot@foo.bar'
            session['user_id'] = '639ff114a951fa2422580cd0'
        yield client


def test_profile_template(client):
    # Test profile route
    url = '/profile'
    response = client.get(url)
    assert response.status_code == 200


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


def test_login_template(client):
    # Test home route
    url = '/login'
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


def test_edit_template(client):
    # Test edit route
    url = '/edit'
    response = client.get(url)
    assert response.status_code == 200
