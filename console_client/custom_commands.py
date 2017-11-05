from console_client.commands import PurePostCommand


class AddTransformation(PurePostCommand):
    name = 'add_transformation'
    url_suffix = '/api/v1/command/metadata/add_transformation'



class AddQuery(PurePostCommand):
    name = 'add_query'
    url_suffix = '/api/v1/command/metadata/add_query'
