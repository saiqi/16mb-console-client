import json
import os
from pathlib import Path


def _get_config_path():
    if '_16MB_CONFIG_FILE' in os.environ:
        return Path(os.getenv('_16MB_CONFIG_FILE'))
    return Path.home().joinpath('.16mb.json')


def _open_config():
    path = _get_config_path()

    if path.exists():
        return json.loads(path.read_text())

    return None


def _save_config(config):
    path = _get_config_path()

    if config:
        path.write_text(json.dumps(config))
        return config

    return None


def _init_config():
    username = input('User: ')
    base_url = input('Base URL Root: ')
    auth_url = input('Auth URL Root: ')

    config = {'username': username, 'base_url': base_url, 'auth_url': auth_url, 'auth_token': ''}

    return config


def get_config(updated_key=None, updated_value=None):
    config = _open_config()

    if config is None:
        config = _init_config()
        _save_config(config)
        return get_config()

    if updated_key is None:
        return config
    else:
        config[updated_key] = updated_value
        _save_config(config)
        return get_config()
