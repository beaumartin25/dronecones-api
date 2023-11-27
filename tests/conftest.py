import sys
import os
import tempfile
# Get the current file's directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# Append the root directory to Python's path
sys.path.append(os.path.join(current_directory, ".."))
# above code was because my pyhton was not finding api or api.db correctly

import pytest
from api import create_app
from api.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()