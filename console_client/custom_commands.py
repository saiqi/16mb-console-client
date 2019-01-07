import json
import requests
import yaml
from console_client.commands import PurePostCommand, CommandById, Command, PureGetCommand, CommandError


class CreateUser(Command):
    name = 'create_user'
    url_suffix = '/users'
    method_verb = 'POST'

    def init_parser(self, parser):
        return parser

    def main(self, args):

        def __input_and_check(label):
            while True:
                x = input('Enter {}: '.format(label))
                check = input('Confim {}: '.format(label))
                if x == check:
                    return x
                print('Mismatched ! Please reenter {}'.format(label))

        user = __input_and_check('user name')
        email = __input_and_check('email')
        while True:
            role = input('Enter role: ')
            if role in ('read', 'write', 'admin',):
                break
            print('Bad value ! Only read, write and admin are supported')
        url = ''.join([self.base_url, self.url_suffix])

        r = requests.post(url, json={'user': user, 'email': email, 'role': role}, headers=self.headers)

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)


class AddSubscription(PurePostCommand):
    name = 'add_subscription'
    url_suffix = '/api/v1/command/subscription/add'


class GetSubscription(CommandById):
    name = 'get_subscription'
    url_suffix = '/api/v1/query/subscription/<id>'
    method_verb = 'GET'


class CreateTable(PurePostCommand):
    name = 'create_table'
    url_suffix = '/api/v1/command/datastore/create_table'


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


class GetAllTransformations(PureGetCommand):
    name = 'all_transformations'
    url_suffix = '/api/v1/query/metadata/transformations'


class DeployFunction(CommandById):
    name = 'deploy_function'
    url_suffix = '/api/v1/command/metadata/deploy_function/<id>'
    method_verb = 'POST'

class AddTrigger(PurePostCommand):
    name = 'add_trigger'
    url_suffix = '/api/v1/command/metadata/add_trigger'


class DeleteTrigger(CommandById):
    name = 'delete_trigger'
    url_suffix = '/api/v1/command/metadata/delete_trigger/<id>'
    method_verb = 'DELETE'


class GetTriggerById(CommandById):
    name = 'get_trigger'
    url_suffix = '/api/v1/query/metadata/trigger/<id>'
    method_verb = 'GET'


class GetAllTriggers(PureGetCommand):
    name = 'all_triggers'
    url_suffix = '/api/v1/query/metadata/triggers'


class AddQuery(PurePostCommand):
    name = 'add_query'
    url_suffix = '/api/v1/command/metadata/add_query'


class DeleteQuery(CommandById):
    name = 'delete_query'
    url_suffix = '/api/v1/command/metadata/delete_query/<id>'
    method_verb = 'DELETE'


class GetQueryById(CommandById):
    name = 'get_query'
    url_suffix = '/api/v1/query/metadata/query/<id>'
    method_verb = 'GET'


class GetAllQueries(PureGetCommand):
    name = 'all_queries'
    url_suffix = '/api/v1/query/metadata/queries'


class AddTemplate(PurePostCommand):
    name = 'add_template'
    url_suffix = '/api/v1/command/metadata/add_template'


class DeleteTemplate(CommandById):
    name = 'delete_template'
    url_suffix = '/api/v1/command/metadata/delete_template/<id>'
    method_verb = 'DELETE'


class GetTemplateById(CommandById):
    name = 'get_template'
    url_suffix = '/api/v1/query/metadata/template/<id>'
    method_verb = 'GET'


class GetAllTemplates(PureGetCommand):
    name = 'all_templates'
    url_suffix = '/api/v1/query/metadata/templates'


class AddQueryToTemplate(Command):
    name = 'add_query_to_template'
    url_suffix = '/api/v1/command/metadata/template/add_query/<id>'
    method_verb = 'POST'

    def init_parser(self, parser):
        parser.add_argument('id', help='Resource Id')
        parser.add_argument('--file', '-f', default='', help='Query configuration file')
        return parser

    def main(self, args):
        try:
            with open(args.file, 'r') as f:
                data = yaml.load(f.read())
        except:
            raise CommandError('Command configuration file not found')

        resolved_suffix = self.url_suffix.replace('<id>', args.id)
        url = ''.join([self.base_url, resolved_suffix])

        r = requests.post(url, data=json.dumps(data), headers=self.headers)

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)


class UpdateHTMLInTemplate(Command):
    name = 'update_html'
    url_suffix = '/api/v1/command/metadata/template/update_html/<id>'
    method_verb = 'POST'

    def init_parser(self, parser):
        parser.add_argument('id', help='Resource Id')
        parser.add_argument('--file', '-f', default='', help='HTML file')
        return parser

    def main(self, args):
        try:
            with open(args.file, 'r') as f:
                html = f.read()
        except:
            raise CommandError('HTML file not found')
        
        resolved_suffix = self.url_suffix.replace('<id>', args.id)
        url = ''.join([self.base_url, resolved_suffix])
        r = requests.post(url, data=json.dumps({'html': html}), headers=self.headers)
        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)


class UpdateSVGInTemplate(Command):
    name = 'update_svg'
    url_suffix = '/api/v1/command/metadata/template/update_svg/<id>'
    method_verb = 'POST'

    def init_parser(self, parser):
        parser.add_argument('id', help='Resource Id')
        parser.add_argument('--file', '-f', default='', help='SVG file')
        return parser

    def main(self, args):
        try:
            with open(args.file, 'r') as f:
                svg = f.read()
        except:
            raise CommandError('HTML file not found')
        
        resolved_suffix = self.url_suffix.replace('<id>', args.id)
        url = ''.join([self.base_url, resolved_suffix])
        r = requests.post(url, data=json.dumps({'svg': svg}), headers=self.headers)
        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)


class DeleteQueryFromTemplate(Command):
    name = 'delete_query_from_template'
    url_suffix = '/api/v1/command/metadata/template/delete_query/<template_id>/<query_id>'
    method_verb = 'DELETE'

    def init_parser(self, parser):
        parser.add_argument('template_id', help='Template Id')
        parser.add_argument('query_id', help='Query Id')

    def main(self, args):
        resolved_suffix = self.url_suffix.replace('<template_id>', args.template_id)\
            .replace('<query_id>', args.query_id)
        url = ''.join([self.base_url, resolved_suffix])

        r = requests.delete(url, headers=self.headers)

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)


class ResolveTemplate(Command):
    name = 'resolve_template'
    url_suffix = '/api/v1/query/metadata/template/resolve_with_ids/<id>'
    method_verb = 'POST'

    def init_parser(self, parser):
        parser.add_argument('id', help='Resource Id')
        parser.add_argument('--file', '-f', default='', help='Parameters file')
        parser.add_argument('--output', '-o', default='result.svg', help='Output SVG name')
        return parser

    def main(self, args):
        resolved_suffix = self.url_suffix.replace('<id>', args.id)
        url = ''.join([self.base_url, resolved_suffix])

        try:
            with open(args.file, 'r') as f:
                data = yaml.load(f.read())
        except:
            raise CommandError('Command configuration file not found')

        r = requests.post(url, headers=self.headers, data=json.dumps(data))

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        with open(args.output, 'w') as f:
            f.write(r.text)

        return 'Done'


class ResolveQuery(Command):
    name = 'resolve_query'
    url_suffix = '/api/v1/query/metadata/query/resolve/<id>'
    method_verb = 'POST'

    def init_parser(self, parser):
        parser.add_argument('id', help='Resource Id')
        parser.add_argument('--file', '-f', default='', help='Parameters file')
        return parser

    def main(self, args):
        resolved_suffix = self.url_suffix.replace('<id>', args.id)
        url = ''.join([self.base_url, resolved_suffix])

        try:
            with open(args.file, 'r') as f:
                data = yaml.load(f.read())
        except:
            raise CommandError('Command configuration file not found')

        r = requests.post(url, headers=self.headers, data=json.dumps(data))

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)


class RefreshTriggers(PurePostCommand):
    name = 'refresh_triggers'
    url_suffix = '/api/v1/command/metadata/triggers/refresh'


class ExportSVG(Command):
    name = 'export_svg'
    url_suffix = '/api/v1/command/export'
    method_verb = 'POST'

    def init_parser(self, parser):
        parser.add_argument('svg', help='SVG file to export')
        parser.add_argument('filename', help='Exported file name')
        parser.add_argument('format', help='File format')
        parser.add_argument('--dpi', '-D', help='Export DPI', type=int)
        return parser

    def main(self, args):
        url = ''.join([self.base_url, self.url_suffix])

        try:
            with open(args.svg, 'r') as f:
                svg = f.read()
        except:
            raise CommandError('SVG file not found')

        data = {
            'svg': svg,
            'filename': args.filename,
            'format': {
                'type': args.format,
                'dpi': args.dpi
            }
        }

        r = requests.post(url, headers=self.headers, data=json.dumps(data))

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)

class AddLabel(Command):
    name = 'add_label'
    url_suffix = '/api/v1/command/referential/add_label'
    method_verb = 'POST'

    def init_parser(self, parser):
        parser.add_argument('--file', '-f', default='', help='Labels file')
        return parser

    def main(self, args):
        url = ''.join([self.base_url, self.url_suffix])

        try:
            with open(args.file, encoding='utf-8') as f:
                data = yaml.load(f.read())
        except:
            raise CommandError('Labels file not found')

        for r in data:
            req = requests.post(url, data=json.dumps(r), headers=self.headers)

            if req.status_code >= 400:
                raise CommandError('Error while processing command {}: {}'.format(self.name, req.text))

        return self.result(req)


class DeleteLabel(Command):
    name = 'delete_label'
    url_suffix = '/api/v1/command/referential/delete_label/<label_id>/<language>/<context>'
    method_verb = 'DELETE'

    def init_parser(self, parser):
        parser.add_argument('label_id', help='Label Id')
        parser.add_argument('language', help='Language')
        parser.add_argument('context', help='Context')

        return parser

    def main(self, args):
        resolved_suffix = self.url_suffix.replace('<label_id>', args.label_id)\
        .replace('<language>', args.language)\
        .replace('<context>', args.context)

        url = ''.join([self.base_url, resolved_suffix])

        r = requests.delete(url, headers=self.headers)

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)


class GetLabel(Command):
    name = 'get_label'
    url_suffix = '/api/v1/query/referential/get_label/<label_id>/<language>/<context>'
    method_verb = 'GET'

    def init_parser(self, parser):
        parser.add_argument('label_id', help='Label Id')
        parser.add_argument('language', help='Language')
        parser.add_argument('context', help='Context')

        return parser

    def main(self, args):
        resolved_suffix = self.url_suffix.replace('<label_id>', args.label_id)\
        .replace('<language>', args.language)\
        .replace('<context>', args.context)

        url = ''.join([self.base_url, resolved_suffix])

        r = requests.get(url, headers=self.headers)

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)


class SearchEntity(Command):
    name = 'search_entity'
    url_suffix = '/api/v1/query/referential/search_entity'
    method_verb = 'GET'

    def init_parser(self, parser):
        parser.add_argument('name', help='Search name')
        parser.add_argument('--type', '-t', help='Entity type')
        parser.add_argument('--provider', '-p', help='Data provider')

        return parser

    def main(self, args):
        url = ''.join([self.base_url, self.url_suffix])

        params = {'name': args.name}
        if args.type:
            params['type'] = args.type

        if args.provider:
            params['provider'] = args.provider

        r = requests.get(url, headers=self.headers, params=params)

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)


class SearchEvent(Command):
    name = 'search_event'
    url_suffix = '/api/v1/query/referential/search_event'
    method_verb = 'GET'

    def init_parser(self, parser):
        parser.add_argument('name', help='Search name')
        parser.add_argument('date', help='Event date')
        parser.add_argument('--type', '-t', help='Entity type')
        parser.add_argument('--provider', '-p', help='Data provider')

        return parser

    def main(self, args):
        url = ''.join([self.base_url, self.url_suffix])

        params = {'name': args.name, 'date': args.date}
        if args.type:
            params['type'] = args.type

        if args.provider:
            params['provider'] = args.provider

        r = requests.get(url, headers=self.headers, params=params)

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)


class FuzzySearch(Command):
    name = 'fuzzy_search'
    url_suffix = '/api/v1/query/referential/search'
    method_verb = 'GET'

    def init_parser(self, parser):
        parser.add_argument('query', help='Search query')
        parser.add_argument('type', help='Entity type')
        parser.add_argument('provider', help='Data provider')

        return parser

    def main(self, args):
        url = ''.join([self.base_url, self.url_suffix])
        params = {'query': args.query, 'type': args.type, 'provider': args.provider}

        r = requests.get(url, headers=self.headers, params=params)

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)


class AddTranslationToEntity(Command):
    name = 'add_translation_to_entity'
    url_suffix = '/api/v1/command/referential/add_translation_to_entity/<id>'
    method_verb = 'POST'

    def init_parser(self, parser):
        parser.add_argument('--file', '-f', default='', help='Command configuration file')
        return parser

    def main(self, args):
        try:
            with open(args.file, encoding='utf-8') as f:
                data = yaml.load(f.read())
        except:
            raise CommandError('Command configuration file not found')

        for r in data:
            resolved_suffix = self.url_suffix.replace('<id>', r['id'])
            url = ''.join([self.base_url, resolved_suffix])
            req = requests.post(url, data=json.dumps(r), headers=self.headers)

            if req.status_code >= 400:
                raise CommandError('Error while processing command {}: {}'.format(self.name, req.text))

        return self.result(req)


class AddMultilineToEntity(Command):
    name = 'add_multiline_to_entity'
    url_suffix = '/api/v1/command/referential/add_multiline_to_entity/<id>'
    method_verb = 'POST'

    def init_parser(self, parser):
        parser.add_argument('--file', '-f', default='', help='Command configuration file')
        return parser

    def main(self, args):
        try:
            with open(args.file, encoding='utf-8') as f:
                data = yaml.load(f.read())
        except:
            raise CommandError('Command configuration file not found')

        for r in data:
            resolved_suffix = self.url_suffix.replace('<id>', r['id'])
            url = ''.join([self.base_url, resolved_suffix])
            req = requests.post(url, data=json.dumps(r), headers=self.headers)

            if req.status_code >= 400:
                raise CommandError('Error while processing command {}: {}'.format(self.name, req.text))

        return self.result(req)


class AddPictureToEntity(Command):
    name = 'add_picture_to_entity'
    url_suffix = '/api/v1/command/referential/add_picture_to_entity/<id>'
    method_verb = 'POST'

    def init_parser(self, parser):
        parser.add_argument('id', help='Entity Id')
        parser.add_argument('context', help='Picture context name (ex: customer name)')
        parser.add_argument('format', help='Picture format name (ex: render, passport ...)')
        parser.add_argument('file', help='Picture filesystem path')

        return parser

    def main(self, args):
        import base64
        with open(args.file, 'rb') as f:
            picture = base64.b64encode(f.read())

        resolved_suffix = self.url_suffix.replace('<id>', args.id)
        url = ''.join([self.base_url, resolved_suffix])

        r = requests.post(url, headers=self.headers, data=json.dumps({
            'id': args.id,
            'context': args.context,
            'format': args.format,
            'picture_b64': picture.decode('utf-8')}))

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)


class DeletePictureFromEntity(Command):
    name = 'delete_picture_from_entity'
    url_suffix = '/api/v1/command/referential/delete_picture_from_entity/<entity_id>/<context>/<format>'
    method_verb = 'DELETE'

    def init_parser(self, parser):
        parser.add_argument('id', help='Entity Id')
        parser.add_argument('context', help='Picture context name (ex: customer name)')
        parser.add_argument('format', help='Picture format name (ex: render, passport ...)')

        return parser

    def main(self, args):
        resolved_suffix = self.url_suffix.replace('<entity_id>', args.id)\
        .replace('<context>', args.context)\
        .replace('<format>', args.format)

        url = ''.join([self.base_url, resolved_suffix])

        r = requests.delete(url, headers=self.headers)

        if r.status_code >= 400:
            raise CommandError('Error while processing command {}: {}'.format(self.name, r.text))

        return self.result(r)