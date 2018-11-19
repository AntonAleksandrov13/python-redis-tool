###IMPORTS###
import argparse
import sys

import ipaddress


class CommandParser(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Python tool for a Redis cluster administration.',
            usage='''redis-tool.py <command> [<args>]''')
        parser.add_argument('command', help='Operation to run. Choices are add_node, reshard, stats')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print 'Unrecognized command'
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def add_node(self):
        parser = argparse.ArgumentParser(
            description='Add node to the given cluster')
        parser.add_argument('-role', choices=['master', 'slave'],
                            help='Role of the node in the cluster. Could be either master or slave')
        args = parser.parse_args(sys.argv[2:])
        print (args)
        print 'Adding node...'

    def reshard(self):
        parser = argparse.ArgumentParser(
            description='Reshard the given cluster.')
        args = parser.parse_args(sys.argv[2:])
        print (args)
        print 'Resharding cluster...'

    def stats(self):
        parser = argparse.ArgumentParser(
            description='Print .')
        args = parser.parse_args(sys.argv[2:])
        print (args)
        print 'Resharding cluster...'



if __name__ == '__main__':
    CommandParser()
