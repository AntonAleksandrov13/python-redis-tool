#!/usr/bin/env python3.7
import argparse
import sys

from cli import reshard, add_node, validate_node
import logging


class CommandParser(object):
    source = ""

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Python tool for a Redis cluster administration.',
            usage='redis_tool.py [-s REDIS_NODE_ADDRESS] [-d] command <args>')
        parser.add_argument('command',
                            help='command to run. Right now there are two options')
        parser.add_argument('-s', '--source', help='one of the nodes from the Redis cluster. '
                                                   'It will be used as an entrypoint to all cluster operations. '
                                                   'If not provided, default address 127.0.0.1:6379 will be used.')
        parser.add_argument('-d', '--debug', default=False, action="store_true",
                            help="sets logging level to Debug(provides more details). "
                                 "If not supplied, Info logging level will be used.")
        if len(sys.argv) == 3:
            args = parser.parse_args(sys.argv[1:2])
            attribute_to_call = args.command

        else:
            options, args = parser.parse_known_args()
            if not hasattr(self, options.command):
                print('Unrecognized command')
                parser.print_help()
                exit(1)
            self.source = "127.0.0.1:6379" if options.source is None else options.source
            logging_level = logging.INFO if options.debug is False else logging.DEBUG
            logging.basicConfig(level=logging_level, format='%(asctime)s %(message)s')
            attribute_to_call = options.command
        getattr(self, attribute_to_call)()

    def add_node(self):
        parser = argparse.ArgumentParser(
            description='This command will add the given target node(s) to the cluster. It simply '
                        'executes add_node command from redis-cli multiple times.',
            usage='redis_tool.py [--source] [--d] add_node -role <master|slave> -target <node_address...>')
        parser.add_argument('-r', '--role', required=True, choices=['master', 'slave'],
                            help='Role of the node in the cluster. Could be either master or slave')

        parser.add_argument('-t', '--target', nargs='+', required=True,
                            help='Address of the node you would like to add to the cluster.')
        options, args = parser.parse_known_args()
        logging.debug('%s have been passed to add_node function', options)
        add_node.add_node_to_cluster(self.source, options.target, options.role)

    def reshard(self):
        parser = argparse.ArgumentParser(
            description='This command is used for resharding a Redis cluster. It works as following: defines cluster '
                        'master nodes which already have hash slots and cluster master nodes without hash slots. Then '
                        'it calculates how to equally distribute hash slots across all masters and performs a set of '
                        'resharding operation using redis-cli.',
            usage='''redis_tool.py [--source] [--d] reshard''')
        parser.parse_known_args()

        reshard.reshard(self.source)

    @staticmethod
    def validate(node_to_validate):
        if not validate_node.is_valid_redis_node(node_to_validate):
            logging.error("[X] Source node is not valid.")
            exit(1)
        logging.info("[√] Source node is valid")


def main():
    CommandParser()


if __name__ == '__main__':
    main()
