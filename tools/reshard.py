import re
import subprocess

from pip._internal import logger

from tools.util import is_ip
from tools import util



def reshard(source):
    logger.info("Started resharding")
    host, port = util.split_address(source)
    cmd_args = ['--csv', '-h', host, '-p', port, 'cluster', 'slots']
    result = util.run_redis_cli_cmd(cmd_args)
    parsed_cmd_result = result.stdout.decode("utf-8").rstrip()
    result_as_array = re.compile(",").split(parsed_cmd_result)
    for i in result_as_array:
        print(i)
    logger.info("[√] Done")

    i = 0
    while i < len(result_as_array):
        if is_ip(result_as_array[i]):
            print(result_as_array[i])
