class LSA:
    def __init__(self, link_state_id, sequence_number, advertising_router, link_cost, timestamp):
        self.link_state_id = link_state_id
        self.sequence_number = sequence_number
        self.advertising_router = advertising_router
        self.link_cost = link_cost
        self.timestamp = timestamp
