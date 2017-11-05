import argparse
import importlib
import inspect
import sys

from console_client.commands import CommandError
from . import custom_commands
from console_client.displayer import display


def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def setup_commands():
    commands = dict()

    module = importlib.import_module('console_client.custom_commands')
    classes = inspect.getmembers(module, inspect.isclass)

    for c in classes:
        _class = getattr(module, c[0])
        if _class.name is not None:
            commands[_class.name] = _class()

    return commands


def setup_parser(commands):
    parser = argparse.ArgumentParser()
    #parser.add_argument('command')

    subparsers = parser.add_subparsers(help='commands choice')

    for name, instance in commands.items():
        command_parser = subparsers.add_parser(name, help='{} help'.format(name))
        try:
            instance.init_parser(command_parser)
        except NotImplementedError:
            continue

    return parser


def main():
    commands = setup_commands()
    parser = setup_parser(commands)
    args = parser.parse_args()

    name = sys.argv[1]
    try:
        cmd = commands[name]
    except KeyError:
        print_error('Unkown command {}'.format(name))
        raise

    try:
        res = cmd.main(args)
    except CommandError as e:
        print_error('An error has occured while processing command: {}'.format(str(e)))
        raise
        
    display(res)
