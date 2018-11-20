###IMPORTS###
import argparse
import sys
import ipaddress
from tools import validate_node


class CommandParser(object):
    sourceHost = ""
    sourcePort = ""

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Python tool for a Redis cluster administration.',
            usage='''redis-tool.py [-host ip_of_any_cluster_node] [-p port_of_the_node] <command> [<args>]''')
        parser.add_argument('command', help='Operation to run. Choices are add_node, reshard, stats, '
                                            'validate_redis_node')
        parser.add_argument('--source_host', help='IP address of any node in the Redis cluster.')
        parser.add_argument('--source_port', type=int, help='Port of the node.')

        options, args = parser.parse_known_args()
        if not hasattr(self, options.command):
            print 'Unrecognized command'
            parser.print_help()
            exit(1)
        self.sourceHost = "127.0.0.1" if options.source_host is None else options.source_host
        self.sourcePort = "6379" if options.source_port is None else options.source_port
        if options.command != "validate":
            self.validate()
        getattr(self, options.command)()

    def add_node(self):
        parser = argparse.ArgumentParser(
            description='Add node to the given cluster')
        parser.add_argument('-role', choices=['master', 'slave'],
                            help='Role of the node in the cluster. Could be either master or slave')
        options, args = parser.parse_known_args()
        print (options)
        print 'Adding node...'

    def reshard(self):
        parser = argparse.ArgumentParser(
            description='Reshard the given cluster.')

        options, args = parser.parse_known_args()
        print (options)
        print 'Resharding cluster...'

    def stats_cluster(self):
        parser = argparse.ArgumentParser(
            description='Print info about cluster.')
        options, args = parser.parse_known_args()
        print (args)
        print 'Printing cluster info...'

    def validate(self):
        print 'Validating redis node...'
        if validate_node.is_valid_redis_node(self.sourceHost):
            print 'Valid redis node...'
        else:
            print 'Not valid...'


if __name__ == '__main__':
    CommandParser()
