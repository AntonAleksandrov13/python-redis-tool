import logging

from tools import util


def add_node_to_cluster(source, target, target_role):
    logging.info('Adding %s with the %s role to the cluster ', target, target_role)

    for redis_node_address in target:
        cmd = ['add-node', redis_node_address, source]
        if target_role == "slave":
            cmd.append("--cluster-slave")
        result = util.run_redis_cli_cmd(cmd)
        if result.returncode == 0:
            logging.info('[√] Node %s was added to the cluster with role %s', redis_node_address, target_role)
        else:
            logging.error(
                '[X] Node %s was NOT added to the cluster. '
                'Check if the given node is in clustered mode or if is it empty',
                redis_node_address)
