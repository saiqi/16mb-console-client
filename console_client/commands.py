import datetime
import json
import getpass

import jwt
import requests
import yaml

from console_client.confighandler import get_config


class CommandError(Exception):
    pass


class Command(object):

    name = None
    url_suffix = None
    method_verb = None

    def __init__(self):
        self._handle_config()

    def _authenticate(self):
        url = ''.join([self.base_url, '/auth'])
        password = getpass.getpass('Password: ')
        r = requests.post(url, data={'user': self.username, 'password': password})

        if r.status_code >= 400:
            raise CommandError('Authentication failed')

        return json.loads(r.text)

    def _handle_config(self):
        config = get_config()
        self.base_url = config['base_url']
        self.username = config['username']

        authentication_needed = False
        auth_token = config['auth_token']

        if auth_token == '':
            authentication_needed = True
        else:
            payload = jwt.decode(auth_token, verify=False)
            expiration = datetime.datetime.fromtimestamp(payload['exp'])
            if  expiration < datetime.datetime.now():
                authentication_needed = True

        if authentication_needed is True:
            auth_token = self._authenticate()
            get_config('auth_token', auth_token)

        self.headers = {'Authorization': auth_token}

    def init_parser(self, parser):
        raise NotImplementedError

    def main(self, args):
        raise NotImplementedError


class PurePostCommand(Command):

    method_verb = 'POST'

    def init_parser(self, parser):
        parser.add_argument('--file', '-f', default='', help='Command configuration file')
        return parser

    def main(self, args):
        try:
            with open(args.file, 'r') as f:
                data = yaml.load(f.read())
        except:
            raise CommandError('Command configuration file not found')

        url = ''.join([self.base_url, self.url_suffix])

        r = requests.post(url, data=json.dumps(data), headers=self.headers)

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return json.loads(r.text)

class CommandById(Command):

    def init_parser(self, parser):
        parser.add_argument('id', help='Resource Id')
        return parser

    def main(self, args):
        resolved_suffix = self.url_suffix.replace('<id>', args.id)
        url = ''.join([self.base_url, resolved_suffix])

        if self.method_verb == 'POST':
            r = requests.post(url, headers=self.headers)
        elif self.method_verb == 'DELETE':
            r = requests.delete(url, headers=self.headers)
        elif self.method_verb == 'GET':
            r = requests.get(url, headers=self.headers)
        elif self.method_verb == 'PUT':
            r = requests.put(url, headers=self.headers)
        else:
            raise CommandError('Unsupported HTTP verb: {}'.format(self.method_verb))
            
        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return json.loads(r.text)
