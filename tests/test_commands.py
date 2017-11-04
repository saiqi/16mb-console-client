import argparse
import json

import requests
import yaml

from console_client.commands import PurePostCommand
from console_client.confighandler import get_config


def test_pure_post_command(monkeypatch, tmpdir, config_file, good_token, expired_token):
    get_config(updated_key='auth_token', updated_value=good_token)

    data = {'id': 'myid'}
    f = tmpdir.mkdir('yaml').join('test.yaml')
    f.write(yaml.dump(data=data))

    cmd = PurePostCommand(name='add_transformation', url_suffix='/myendpoint')

    parser = argparse.ArgumentParser()
    parser = cmd.init_parser(parser)
    args = parser.parse_args([
        '--file',
        f.strpath
    ])

    def mockpost(url, data, headers):
        class MockResponse(object):
            def __init__(self, url, data, headers):
                self.text = json.dumps({'id': 'myid'})
                self.status_code = 201
                self.url = url
                self.data = data
                self.headers = headers
        return MockResponse(url, data, headers)

    monkeypatch.setattr(requests, 'post', mockpost)
    result = cmd.main(args)
    assert result['id'] == 'myid'