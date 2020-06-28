import datetime
import json
import getpass
import os
import jwt
import requests
import yaml

from console_client.confighandler import get_config
from console_client.displayer import print_error


class CommandError(Exception):
    pass


class Command(object):

    name = None
    url_suffix = None
    method_verb = None

    def __init__(self):
        self._handle_config()

    def _authenticate(self):
        url = ''.join([self.auth_url, '/auth'])
        password = getpass.getpass('Password: ')
        r = requests.post(url, data={'user': self.username, 'password': password})

        if r.status_code >= 400:
            raise CommandError('Authentication failed')

        return json.loads(r.text)

    def _handle_config(self):
        config = get_config()
        self.base_url = config['base_url']
        self.username = config['username']
        self.auth_url = config.get('auth_url', self.base_url)

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

    def result(self, response):
        try:
            return json.loads(response.text)
        except:
            return response.text


class PurePostCommand(Command):

    method_verb = 'POST'

    def init_parser(self, parser):
        parser.add_argument('--file', '-f', default='', help='Command configuration file')
        return parser

    def execute(self, filename):
        try:
            with open(filename, 'r') as f:
                data = yaml.load(f.read())
        except:
            raise CommandError('Command configuration file not found')

        url = ''.join([self.base_url, self.url_suffix])

        r = requests.post(url, data=json.dumps(data), headers=self.headers)

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)

    def main(self, args):
        return self.execute(args.file)


class PureGetCommand(Command):

    method_verb = 'GET'

    def init_parser(self, parser):
        return parser

    def main(self, args):
        url = ''.join([self.base_url, self.url_suffix])

        r = requests.get(url, headers=self.headers)

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)


class CommandById(Command):

    def init_parser(self, parser):
        parser.add_argument('id', help='Resource Id')
        return parser

    def execute(self, id_):
        resolved_suffix = self.url_suffix.replace('<id>', id_)
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

        return self.result(r)

    def main(self, args):
        return self.execute(args.id)


class CommandBundle(Command):
    
    file_command = None
    next_command = None
    next_resource_key = None

    def init_parser(self, parser):
        parser.add_argument('directory', help='Directory location')
        return parser

    def get_files(self, directory):
        for cur, _, files in os.walk(directory):
            for f in sorted(files):
                yield os.path.join(cur, f)

    def main(self, args):
        assert(isinstance(self.file_command, PurePostCommand))
        directory = args.directory

        resp = []
        for f in self.get_files(directory):
            try:
                r = self.file_command.execute(f)
            except CommandError as e:
                print_error(str(e))
                continue
            
            if self.next_command:
                assert(isinstance(self.next_command, CommandById))
                try:
                    resource_id = r[self.next_resource_key or 'id']
                except KeyError:
                    raise CommandError('Cannot find resource key in previous command result!')
                
                try:
                    self.next_command.execute(resource_id)
                except CommandError as e:
                    print_error('{}: {}'.format(resource_id, str(e)))
                    continue

            resp.append(r)
        
        return resp