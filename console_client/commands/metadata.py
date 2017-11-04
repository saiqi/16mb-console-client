from console_client.commands import PurePostCommand


class AddTransformationCommand(PurePostCommand):

    def __init__(self):
        super(PurePostCommand, self).__init__(name='add_transformation',
                                              url_suffix='/api/v1/command/metadata/add_transformation')
