class MasterNode(object):
    start_slot = 0
    end_slot = 0
    ip = ""
    port = 0
    id = ""

    def __init__(self, start_slot, end_slot, ip, port, id):
        self.start_slot = start_slot
        self.end_slot = end_slot
        self.ip = ip
        self.port = port
        self.id = id
