import sys
sys.path.append('.')
print(sys.path)

from app import app
from flask import Flask, render_template
import pytest
import pytest_flask
import pymongo
import mongomock
from pymongo import MongoClient
import os

def test_base_template():
    # Test login route
    client = app.test_client()
    url = '/'
    response = client.get(url)
    assert response.status_code == 200

def test_job_notexist_template():
    # Test a job that does not exist
    client = app.test_client()
    url = '/job/00000000'
    response = client.get(url)
    assert response.status_code == 404

def test_job_template():
    # Test a job
    client = app.test_client()
    url = '/job/63850f2eb4f144d4df2fc305'
    response = client.get(url)
    assert response.status_code == 404

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

def test_home_template():
    # Test home route
    client = app.test_client()
    url = '/home'
    response = client.get(url)
    assert response.status_code == 200

def get_db():
    cxn = pymongo.MongoClient(os.environ['MONGODB_URI'],serverSelectionTimeoutMS=5000)
    db = cxn.get_default_database()
    return db

def db_text_add():
    db = get_db()
    db.test_collection.insert_one({"user_id": "test", "user_name": "test"})
    assert db.test_collection.find_one({"user_id": "test", "user_name": "test"}) is not None











