from console_client.commands import PurePostCommand


class AddTransformationCommand(PurePostCommand):
    name = 'add_transformation'
    url_suffix = '/api/v1/command/metadata/add_transformation'
