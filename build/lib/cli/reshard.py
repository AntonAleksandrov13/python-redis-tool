import re
import time

from pip._internal import logger

from cli.util import validate
from cli.util import split_address
from cli.util import run_redis_cli_cmd
from cli.master_node import MasterNode
from cli.util import is_ip


def reshard(source):
    validate(source)
    logger.info("Started resharding")
    host, port = split_address(source)
    cluster_masters_without_slots, cluster_masters_with_slots = get_slot_distribution(host, port)
    logger.debug('Found %s master(s) in the cluster with slots', len(cluster_masters_with_slots))
    logger.debug('Found %s master(s) in the cluster without slots', len(cluster_masters_without_slots))
    if len(cluster_masters_without_slots) == 0:
        logger.error('Cannot start resharding, since there are no masters where slots could be placed')
        return
    logger.info('Performing resharding...')
    perform_resharding(cluster_masters_with_slots, cluster_masters_without_slots, source)
    logger.info('[V] Done resharding')


def get_slot_distribution(host, port):
    cmd_args = ['-c', '-h', host, '-p', port, 'cluster', 'nodes']
    result = run_redis_cli_cmd(cmd_args, True)
    result_as_array = parse_cmd_output_to_array(result.stdout)
    return extract_cluster_masters(result_as_array)


def parse_cmd_output_to_array(stdout):
    parsed_cmd_result = stdout.decode("utf-8")
    parsed_cmd_result.replace('"', '')
    parsed_cmd_result.replace("'", "")
    parsed_cmd_result.rstrip()
    return re.compile("\n").split(parsed_cmd_result)


def extract_cluster_masters(array_of_all_nodes):
    master_nodes_with_slots = []
    master_nodes_without_slots = []
    i = 0
    while i < len(array_of_all_nodes):
        node = array_of_all_nodes[i]
        if not ('slave' in node or 'noaddr' in node):
            node_as_array = re.compile(' ').split(node)
            if 9 >= len(node_as_array) > 1:
                master_node_to_add = process_array_with_master_node_fields(node_as_array)
                if master_node_to_add is not None:
                    if len(node_as_array) == 9:
                        master_nodes_with_slots.append(master_node_to_add)
                    else:
                        master_nodes_without_slots.append(master_node_to_add)
        i += 1
    return master_nodes_without_slots, master_nodes_with_slots


def process_array_with_master_node_fields(node_properties_as_array):
    host, port = split_address(node_properties_as_array[1])
    if is_ip(host):
        start_slot = 0
        end_slot = 0
        if len(node_properties_as_array) is 9:
            start_slot, end_slot = process_start_end_slots(node_properties_as_array[8])
        master_node = MasterNode(start_slot, end_slot, host,
                                 int(port), node_properties_as_array[0])
        logger.debug(master_node)
        return master_node
    return None


def process_start_end_slots(start_end_slot_to_parse):
    start_end_slot = re.split("-", start_end_slot_to_parse)

    return int(start_end_slot[0]), int(start_end_slot[1])


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
            run_redis_cli_cmd(cmd_args, False)
            logger.debug('Soon will run sanity check')
            time.sleep(5)
            cmd_args = ['--cluster', 'fix', master_without_slots.ip + ":" + str(master_without_slots.port)]
            result = run_redis_cli_cmd(cmd_args, True)
            logger.debug('Sanity check returned code %s' % (str(result.returncode)))

        i += 1
