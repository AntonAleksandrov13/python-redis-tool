import re
import subprocess

import logging

def split_address(address):
    address = address.split("@", 1)[0]
    parsed_node_address = re.split(":", address)
    host = parsed_node_address[0]
    port = "6379" if len(parsed_node_address) == 1 else parsed_node_address[1]
    return host, port


def run_redis_cli_cmd(cmd_args, show_output):
    cmd = ['redis-cli']

    for cmd_to_insert in cmd_args:
        cmd.append(cmd_to_insert)
    if not show_output:
        subprocess.call(cmd)
    else:
        return subprocess.run(cmd, stdout=subprocess.PIPE)


def is_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def validate(node_to_validate):
    if not is_valid_redis_node(node_to_validate):
        logging.error("[X] Node %s is not valid." % node_to_validate)
        exit(1)
    logging.info("[V] Node %s is valid" % node_to_validate)


def is_valid_redis_node(node_address):
    logging.debug('Validating connection to the %s', node_address)
    host, port = split_address(node_address)
    cmd_args = ['-c', '-h', host, '-p', port, 'ping']
    result = run_redis_cli_cmd(cmd_args, True)
    parsed_cmd_result = result.stdout.decode("utf-8").rstrip()
    if parsed_cmd_result == "PONG":
        cmd_args = ['-c', '-h', host, '-p', port, 'cluster', 'info']
        result = run_redis_cli_cmd(cmd_args, True)
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
