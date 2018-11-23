import re
import time

from pip._internal import logger

from cli.master_node import MasterNode
from cli.util import is_ip
from cli import util


def reshard(source):
    logger.info("Started resharding")
    host, port = util.split_address(source)
    cluster_masters_with_slots = get_slot_distribution(host, port)
    logger.debug('Found %s master(s) in the cluster with slots', len(cluster_masters_with_slots))
    cluster_masters_without_slots = get_master_without_slots(host, port)
    logger.debug('Found %s master(s) in the cluster without slots', len(cluster_masters_without_slots))
    if len(cluster_masters_without_slots) == 0:
        logger.error('Cannot start resharding, since there are no masters where slots could be placed')
        return
    logger.info('Performing resharding...')
    perform_resharding(cluster_masters_with_slots, cluster_masters_without_slots, source)
    logger.info('[√] Done resharding')


def get_slot_distribution(host, port):
    cmd_args = ['-c', '-h', host, '-p', port, 'cluster', 'slots']
    result = util.run_redis_cli_cmd(cmd_args, True)
    result_as_array = parse_cmd_output_to_array(result.stdout)
    return extract_cluster_masters_with_slots(result_as_array)


def parse_cmd_output_to_array(stdout):
    parsed_cmd_result = stdout.decode("utf-8")
    parsed_cmd_result.replace('"', '')
    parsed_cmd_result.replace("'", "")
    parsed_cmd_result.rstrip()
    return re.compile("\n").split(parsed_cmd_result)


def extract_cluster_masters_with_slots(array_of_all_nodes):
    master_nodes = []
    i = 0
    while i < len(array_of_all_nodes):
        element = array_of_all_nodes[i]
        if is_ip(element):
            try:
                master_node_to_add = MasterNode(int(array_of_all_nodes[i - 2]), int(array_of_all_nodes[i - 1]),
                                                array_of_all_nodes[i],
                                                int(array_of_all_nodes[i + 1]), array_of_all_nodes[i + 2])
                logger.debug(master_node_to_add)
                master_nodes.append(master_node_to_add)
                i += 3
                continue
            except (TypeError, ValueError):
                i += 1
                continue

        i += 1

    return master_nodes


def get_master_without_slots(host, port):
    cmd_args = ['-c', '-h', host, '-p', port, 'cluster', 'nodes']
    result = util.run_redis_cli_cmd(cmd_args, True)
    result_as_array = parse_cmd_output_to_array(result.stdout)
    return extract_masters_without_slots(result_as_array)


def extract_masters_without_slots(all_nodes):
    master_nodes_to_return = []
    i = 0
    while i < len(all_nodes):
        node = all_nodes[i]
        if not ('slave' in node or 'noaddr' in node):
            node_as_array = re.compile(' ').split(node)
            if 8 >= len(node_as_array) > 1:
                host, port = util.split_address(node_as_array[1])
                if is_ip(host):
                    master_node_to_add = MasterNode(0, 0, host,
                                                    int(port), node_as_array[0])
                    logger.debug(master_node_to_add)
                    master_nodes_to_return.append(master_node_to_add)
        i += 1
    return master_nodes_to_return


def perform_resharding(masters_with_slots, masters_without_slots, source):
    amount_of_masters = len(masters_with_slots) + len(masters_without_slots)
    i = 0
    for master_with_slots in masters_with_slots:
        shards_amount_master_will_give = master_with_slots.calculate_amount_of_shards(amount_of_masters)

        logger.debug("%s will give %s shards per split" % (master_with_slots, shards_amount_master_will_give))

        shards_amount_per_one_master = int(shards_amount_master_will_give)

        for master_without_slots in masters_without_slots:
            cmd_args = ['--cluster', 'reshard', source, '--cluster-from', master_with_slots.node_id,
                        '--cluster-to', master_without_slots.node_id, '--cluster-slots',
                        str(shards_amount_per_one_master),
                        '--cluster-yes']
            logger.debug("Sharding %s to %s %s slots" % (
                master_with_slots.node_id, master_without_slots.node_id, shards_amount_per_one_master))
            util.run_redis_cli_cmd(cmd_args, False)
            logger.debug('Soon will run sanity check')
            time.sleep(5)
            cmd_args = ['--cluster', 'fix', master_without_slots.ip + ":" + str(master_without_slots.port)]
            result = util.run_redis_cli_cmd(cmd_args, True)
            logger.debug('Sanity check returned code %s' % (str(result.returncode)))

        i += 1
