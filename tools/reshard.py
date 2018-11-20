import subprocess

from pip._internal import logger

from tools import util


def reshard(source):
    logger.info("Started resharding")
    # host, port = util.split_address(source)
    # cmd_args = ['--csv','-h', host, '-p', port, 'cluster', 'slots']
    # result = util.run_redis_cli_cmd(cmd_args)
    # parsed_cmd_result = result.stdout.decode("utf-8")
    logger.info("[√] Done")
