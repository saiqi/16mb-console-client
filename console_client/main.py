import argparse
import importlib
import sys


def print_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    command = sys.argv[1].split('.')

    try:
        module_name = command[0]
        class_name = command[1]
    except IndexError:
        print_error('Wrong command format: module.ClassName expected')
        sys.exit(1)

    module = importlib.import_module('console_client.commands.{}'.format(module_name))
    _class = getattr(module, class_name)
    cmd = _class()

    parser = argparse.ArgumentParser()
    parser = cmd.init_parser(parser)
    args = parser.parse()
    cmd.main(args)
