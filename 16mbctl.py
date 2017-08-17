import argparse
import getpass
import json
import sys
from pathlib import Path

import requests
from terminaltables import AsciiTable


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
    path.write_text(json.dumps(config))

    return config


def _pretify_json(content):
    data = json.loads(content)
    if isinstance(data, list):
        cpt = 0
        rows = list()
        for row in data:
            if cpt == 0:
                rows.append(sorted(row.keys()))

            rows.append([row[k] for k in sorted(row.keys())])

            cpt += 1

        return AsciiTable(rows)


def _make_request(verb, url, data, headers, config, retry=False):
    print("Requesting URL {}".format(url))

    if verb == 'POST':
        r = requests.post(url, data=json.dumps(data), headers=headers)
        result = r.text
    else:
        if data:
            r = requests.get(url, data=json.dumps(data), headers=headers)
        else:
            r = requests.get(url, headers=headers)
        result = _pretify_json(r.text)

    if r.status_code == 401:
        if retry is False:
            config = _refresh_token(config)
            _make_request(verb, url, data, headers, config, retry=True)
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

    return result


def _handle_parameters(params):
    if params is None:
        return None
    cute_params = dict()
    for p in params:
        kv = p.split('=')
        cute_params[kv[0]] = kv[1]
    return cute_params


def _handle_command(command, domain, config, datafile, params):
    data = None
    if datafile:
        with open(datafile, 'r') as f:
            data = json.loads(f.read())

    headers = {'Authorization': config['token']}

    if command in ('add', 'delete',):
        url = ''.join([config['url_root'], '/api/v1/command/{}/{}'.format(domain, command)])
        result = _make_request('POST', url, data, headers, config)
        print(result)
    elif command == 'get':
        url = ''.join([config['url_root'], '/api/v1/query/{}'.format(domain)])
        result = _make_request('GET', url, _handle_parameters(params), headers, config)
        print(result.table)
    else:
        print('Unknown command type: {}'.format(command))
        sys.exit(1)

if __name__ == '__main__':
    config = _handle_config()

    parser = argparse.ArgumentParser('Toolkit for 16Megabytes API')
    parser.add_argument('command', choices=['get', 'add', 'delete'],
                        help='command type (add: create or update, get: read, delete: remove)')
    parser.add_argument('domain', help='related domain')
    parser.add_argument('--file', '-f', help='JSON format datafile')
    parser.add_argument('--param', '-p', help='parameters JSON string', action='append')

    args = parser.parse_args()

    command = args.command
    domain = args.domain
    datafile = args.file
    params = args.param

    _handle_command(command, domain, config, datafile, params)
