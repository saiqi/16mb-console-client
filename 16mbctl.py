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
    path.write_text(json.dumps(config))

    return config


def _pretify_json(content):
    data = json.loads(content)
    result = None
    if isinstance(data, list):
        cpt = 0
        rows = list()
        for row in data:
            if cpt == 0:
                rows.append('\t\t\t'.join(row.keys()))

            rows.append('\t\t\t'.join([row[k] for k in row.keys()]))

            cpt += 1

        result = '\n'.join(rows)

    return result


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


def _handle_command(command, domain, subcommand, config, datafile=None):
    data = None
    if datafile:
        with open(datafile, 'r') as f:
            data = json.loads(f.read())

    headers = {'Authorization': config['token']}

    if command == 'cmd':
        url = ''.join([config['url_root'], '/api/v1/command/{}/{}'.format(domain, subcommand)])
        result = _make_request('POST', url, data, headers, config)
    elif command == 'get':
        url = ''.join([config['url_root'], '/api/v1/query/{}/{}'.format(domain, subcommand)])
        result = _make_request('GET', url, data, headers, config)
    else:
        print('Unknown command type: {}'.format(command))
        sys.exit(1)

    print(result)

if __name__ == '__main__':
    config = _handle_config()

    if len(sys.argv) < 1:
        print('Wrong arguments. Usage <cmd|get> ...')
        sys.exit(1)

    command = sys.argv[1]
    domain = sys.argv[2]
    subcommand = sys.argv[3]
    datafile = None
    if len(sys.argv) > 4:
        datafile = sys.argv[4]

    _handle_command(command, domain, subcommand, config, datafile)
