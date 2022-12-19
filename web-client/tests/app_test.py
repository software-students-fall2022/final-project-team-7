import os
sys.path.append('.')
import mongomock
import pymongo
import pytest_flask
import pytest
from flask import Flask, render_template
from app import app
import sys
print(sys.path)


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


def test_profile_template():
    # Test profile route
    client = app.test_client()
    url = '/profile'
    response = client.get(url)
    assert response.status_code == 404


def test_edit_template():
    # Test edit route
    client = app.test_client()
    url = '/edit'
    response = client.get(url)
    assert response.status_code == 404
