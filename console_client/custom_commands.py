import json
import requests
from console_client.commands import PurePostCommand, CommandById, Command


class AddTransformation(PurePostCommand):
    name = 'add_transformation'
    url_suffix = '/api/v1/command/metadata/add_transformation'


class DeleteTransformation(CommandById):
    name = 'delete_transformation'
    url_suffix = '/api/v1/command/metadata/delete_transformation/<id>'
    method_verb = 'DELETE'

    
class GetTransformationById(CommandById):
    name = 'get_transformation'
    url_suffix = '/api/v1/query/metadata/transformation/<id>'
    method_verb = 'GET'


class AddQuery(PurePostCommand):
    name = 'add_query'
    url_suffix = '/api/v1/command/metadata/add_query'
    
    
class GetLogs(Command):
    name = 'get_logs'
    url_suffix = '/api/v1/query/crontask/logs'
    method_verb = 'GET'
    
    def init_parser(self, parser):
        parser.add_argument('--method', '-m', default='', help='Method name')
        parser.add_argument('--tail', '-t', default='', help='Tail logs')
        return parser
        
    def main(self, args):
        url = ''.join([self.base_url, self.url_suffix])
        params = dict()
        if args.method != '':
            params['method_name'] = args.method
        if args.tail != '':
            params['tail'] = args.tail
        if params:
            r = requests.get(url, headers=self.headers, params=params)
        else:
            r = requests.get(url, headers=self.headers)
            
        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return json.loads(r.text)
