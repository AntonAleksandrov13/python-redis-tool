import re
import subprocess


def split_address(address):
    parsed_node_address = re.split(":", address)
    host = parsed_node_address[0]
    port = "6379" if len(parsed_node_address) == 1 else parsed_node_address[1]
    return host, port


def run_redis_cli_cmd(cmd_args):
    cmd = ['redis-cli', '-c']
    for cmd_to_insert in cmd_args:
        cmd.append(cmd_to_insert)
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
