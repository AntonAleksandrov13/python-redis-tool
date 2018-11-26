import re
import subprocess

import logging
from cli.validate_node import is_valid_redis_node


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
