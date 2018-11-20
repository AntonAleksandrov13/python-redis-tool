import re
import subprocess


def is_valid_redis_node(node_address):
    parsed_node_address = re.split(":", node_address)
    host = parsed_node_address[0]
    port = "6379" if len(parsed_node_address) == 1 else parsed_node_address[1]
    result = subprocess.run(['redis-cli', '-h', host, '-p', port, 'ping'], stdout=subprocess.PIPE)
    resultAsString = result.stdout.decode("utf-8").rstrip()
    if resultAsString in "PONG":
        return True
    return False
