import json

from console_client.confighandler import get_config


def test_get_config(config_file):
    config = get_config()
    content = json.loads(config_file.read_text())
    assert content == config

    config = get_config('username', 'test2')
    content = json.loads(config_file.read_text())
    assert content == config
