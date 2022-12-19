import sys
sys.path.append('.')
print(sys.path)

import os
from app import app
from flask import Flask, render_template
import pytest
import pytest_flask
import pymongo
import mongomock

sys.path.remove('.')

def test_base_template():
    # Test login route
    client = app.test_client()
    url = '/'
    response = client.get(url)
    assert response.status_code == 302


def test_error_template():
    # Test a route that does not exist
    client = app.test_client()
    url = '/errornotexist'
    response = client.get(url)
    assert response.status_code == 404


def test_register_template():
    # Test register route
    client = app.test_client()
    url = '/register'
    response = client.get(url)
    assert response.status_code == 200


def test_login_template():
    # Test login route
    client = app.test_client()
    url = '/login'
    response = client.get(url)
    assert response.status_code == 200


def test_history_template():
    # Test history route
    client = app.test_client()
    url = '/history'
    response = client.get(url)
    assert response.status_code == 308


def test_history_range_template():
    # Test history route
    client = app.test_client()
    url = '/history/all'
    response = client.get(url)
    assert response.status_code == 200

    url = '/history/today'
    response = client.get(url)
    assert response.status_code == 200

    url = '/history/this_week'
    response = client.get(url)
    assert response.status_code == 200


def test_profile_template(app_with_user):
    url = '/profile'
    response = app_with_user.get(url)
    assert response.status_code == 200


def test_edit_template(app_with_user):
    # Test edit route
    url = '/edit'
    response = app_with_user.get(url)
    assert response.status_code == 200
