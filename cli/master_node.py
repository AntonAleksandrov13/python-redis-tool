class MasterNode(object):
    start_slot = 0
    end_slot = 0
    ip = ""
    port = 0
    node_id = ""

    def __init__(self, start_slot, end_slot, ip, port, node_id):
        if not isinstance(start_slot, int):
            raise TypeError("start_slot must be set to an integer")
        self.start_slot = start_slot
        if not isinstance(end_slot, int):
            raise TypeError("start_slot must be set to an integer")
        self.end_slot = end_slot
        self.ip = ip
        if not isinstance(port, int):
            raise TypeError("port must be set to an integer")
        self.port = port
        if not isinstance(node_id, str):
            raise TypeError("node_id must be set to a string")
        self.node_id = node_id

    def calculate_amount_of_shards(self, amount_of_masters):
        return int((self.end_slot - self.start_slot) / amount_of_masters)

    def __str__(self):
        return 'Node: start_slot:%s, end_slot:%s, node_address:%s:%s, id:%s' % (
            self.start_slot, self.end_slot, self.ip, self.port, self.node_id)
