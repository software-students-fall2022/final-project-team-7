import sys
sys.path.append('.')
print(sys.path)

from app import db, app
import mongomock
import pytest
# start flask app test mode


@pytest.fixture(scope='session')
def flask_app():
    app.config.update({'TESTING': True})
    with app.test_client() as client:
        yield client

# create a fake database


@pytest.fixture(scope='session')
def app_with_database(flask_app):
    db = mongomock.MongoClient().db
    yield flask_app

# create a fake user


@pytest.fixture(scope='session')
def app_with_user(app_with_database):
    db.insert_one({"username": "test", "password":  "test", "reg_date":  "test",
                   "num_chat": 0, "ast_online":  "test", "log_time":  "test"})
    yield app_with_database
