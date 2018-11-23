import logging

from cli import util


def is_valid_redis_node(node_address):
    logging.debug('Validating connection to the %s', node_address)
    host, port = util.split_address(node_address)
    cmd_args = ['-c', '-h', host, '-p', port, 'ping']
    result = util.run_redis_cli_cmd(cmd_args, True)
    parsed_cmd_result = result.stdout.decode("utf-8").rstrip()
    if parsed_cmd_result == "PONG":
        cmd_args = ['-c', '-h', host, '-p', port, 'cluster', 'info']
        result = util.run_redis_cli_cmd(cmd_args, True)
        parsed_cmd_result = result.stdout.decode("utf-8").rstrip()
        if parsed_cmd_result.find("cluster_size:0") >= 0:
            logging.error(
                'Managed to establish a connection with the %s node. But node is a part of an empty redis cluster',
                node_address)
            return False
        logging.debug('Successfully established connection to %s', node_address)
        return True
    logging.error('Could not establish connection with the %s node. Returned code: %s', node_address,
                  result.returncode)
    return False
