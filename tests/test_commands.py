import argparse
import json

import requests
import yaml

from console_client.commands import PurePostCommand
from console_client.confighandler import get_config


def test_pure_post_command(mocker, tmpdir, config_file, good_token):
    get_config(updated_key='auth_token', updated_value=good_token)

    data = {'id': 'myid'}
    f = tmpdir.mkdir('yaml').join('test.yaml')
    f.write(yaml.dump(data=data))

    cmd = PurePostCommand()
    cmd.url_suffix = '/myendpoint'
    cmd.name = 'my_command'

    parser = argparse.ArgumentParser()
    parser = cmd.init_parser(parser)
    args = parser.parse_args([
        '--file',
        f.strpath
    ])

    class MockResponse(object):
        def __init__(self):
            self.text = json.dumps({'id': 'myid'})
            self.status_code = 201

    url = ''.join([cmd.base_url, cmd.url_suffix])
    request_data = json.dumps(data)
    headers = {'Authorization': good_token}
    mocker.patch('requests.post', side_effect=lambda url, data, headers: MockResponse())
    result = cmd.main(args)
    requests.post.assert_called_once_with(url, data=request_data, headers=headers)
    assert result['id'] == 'myid'
