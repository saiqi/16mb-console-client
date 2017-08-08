import requests
from pathlib import Path
import sys
import json
import getpass


def _authenticate(username, url_root):
    password = getpass.getpass('Password: ')

    r = requests.post(''.join([url_root, '/auth']), data={'user': username, 'password': password})

    if r.status_code >= 400:
        print('Authentication failed')
        sys.exit(1)

    return json.loads(r.text)


def _handle_config():
    path = Path.home().joinpath('.16mb.json')

    if path.exists():
        config = json.loads(path.read_text())
    else:
        username = input('User: ')
        url_root = input('URL root: ')

        token = _authenticate(username, url_root)

        config = {'username': username, 'url_root': url_root, 'token': token}
        path.write_text(json.dumps(config))

    return config


def _refresh_token(config):
    config['token'] = _authenticate(config['username'], config['url_root'])
    path = Path.home().joinpath('.16mb.json')
    path.write_text()

    return config


def _make_post_request(url, data, headers, config, retry=False):
    print("Requesting URL {}".format(url))

    r = requests.post(url, data=json.dumps(data), headers=headers)

    if r.status_code == 401:
        if retry is False:
            config = _refresh_token(config)
            _make_post_request(url, data, headers, config, retry=True)
        else:
            print('Authentication failed')
            sys.exit(1)
    elif r.status_code == 403:
        print('Unauthorized')
        sys.exit(1)
    elif r.status_code == 400:
        print('Bad request')
        sys.exit(1)
    elif r.status_code == 404:
        print('Not found')
        sys.exit(1)
    elif r.status_code not in (200, 201):
        print('Something goes wrong')
        sys.exit(1)

    return r.text


def _handle_command(domain, subcommand, datafile, config):
    with open(datafile, 'r') as f:
        data = json.loads(f.read())

    headers = {'Authorization': config['token']}
    url = ''.join([config['url_root'], '/api/v1/command/{}/{}'.format(domain, subcommand)])

    result = _make_post_request(url, data, headers, config)

    print(result)

if __name__ == '__main__':
    config = _handle_config()

    if len(sys.argv) != 4:
        print('Wrong arguments. Usage <domain> <subcommand> <datafile>.json')
        sys.exit(1)

    domain = sys.argv[1]
    subcommand = sys.argv[2]
    datafile = sys.argv[3]

    _handle_command(domain, subcommand, datafile, config)
