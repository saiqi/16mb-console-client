import datetime
import json
import os
import pathlib

import jwt
import pytest


@pytest.fixture
def good_token():
    expiration = datetime.datetime.now() + datetime.timedelta(days=1)
    yield jwt.encode({'exp': expiration}, 'secret', algorithm='HS256').decode('utf-8')


@pytest.fixture
def expired_token():
    expiration = datetime.datetime.now() - datetime.timedelta(days=1)
    yield jwt.encode({'exp': expiration}, 'secret', algorithm='HS256').decode('utf-8')


@pytest.fixture
def config_file():
    path = pathlib.Path(os.getenv('DSAS_CONFIG_FILE'))
    content = json.dumps({
        'username': 'test',
        'base_url': 'http://myurl',
        'auth_token': ''
    })
    path.write_text(content)
    yield path
