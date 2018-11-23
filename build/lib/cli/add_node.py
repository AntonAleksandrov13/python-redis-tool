import logging

from cli import util
from cli.util import is_ip


def add_node_to_cluster(source, target, target_role):
    for redis_node_address in target:
        host, port = util.split_address(redis_node_address)
        if is_ip(host):
            logging.info('Adding %s with the %s role to the cluster ', target, target_role)
            full_node_address = host + ":" + str(port)
            cmd = ['--cluster', 'add-node', full_node_address, source]
            if target_role == "slave":
                cmd.append("--cluster-slave")
            result = util.run_redis_cli_cmd(cmd, True)
            if result.returncode == 0:
                logging.info('[√] Node %s was added to the cluster with role %s', full_node_address, target_role)
            else:
                logging.error(
                    '[X] Node %s was NOT added to the cluster. '
                    'Check if the given node is in clustered mode, '
                    'if is it empty or if this node is already part of the cluster',
                    full_node_address)
        else:
            logging.error(
                '[X] %s node does not have a valid address', target)
