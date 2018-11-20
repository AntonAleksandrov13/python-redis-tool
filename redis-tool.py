###IMPORTS###
import argparse

from tools import validate_node
from tools import add_node
from tools import reshard
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')


class CommandParser(object):
    source = ""

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Python tool for a Redis cluster administration.',
            usage='''redis-tool.py [--source address of any cluster node]  <command> [<args>]''')
        parser.add_argument('command', help='Operation to run. Choices are add_node, reshard, stats, '
                                            'validate_redis_node')
        parser.add_argument('--source', help='Address of any node in the Redis cluster.'
                                             'It will be used as an entry point to cluster operations')

        options, args = parser.parse_known_args()
        if not hasattr(self, options.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        self.source = "127.0.0.1" if options.source is None else options.source
        if options.command != "validate":
            self.validate(self.source)
        getattr(self, options.command)()

    def add_node(self):
        parser = argparse.ArgumentParser(
            description='Add node to the given cluster')
        parser.add_argument('-role', required=True, choices=['master', 'slave'],
                            help='Role of the node in the cluster. Could be either master or slave')

        parser.add_argument('-target', nargs='+', required=True,
                            help='Address of the node you would like to add to the cluster.')
        options, args = parser.parse_known_args()
        logging.debug('%s have been passed to add_node function', options)
        add_node.add_node_to_cluster(self.source, options.target, options.role)

    def reshard(self):
        reshard.reshard(self.source)

    @staticmethod
    def stats_cluster():
        parser = argparse.ArgumentParser(
            description='Print info about cluster.')
        options, args = parser.parse_known_args()
        print(args)
        print('Printing cluster info...')

    @staticmethod
    def validate(node_to_validate):
        if not validate_node.is_valid_redis_node(node_to_validate):
            exit(1)


if __name__ == '__main__':
    CommandParser()
