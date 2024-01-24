import heapq
from datetime import datetime
from lsa import LSA
import socket
import threading
import json

class OSPFRouter:
    def __init__(self, router_id, ip_address, port):
        self.router_id = router_id
        self.ip_address = ip_address  # Added IP address attribute
        self.port = port
        self.connections = {}  # Other OSPFRouters
        self.lsdb = {}
        self.forwarded_lsas = set()
        self.last_message_number = 0

    def start(self):
        # Start the router's networking capabilities
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip_address, self.port))
        self.socket.bind((self.ip_address, self.port))

        # Start a thread for listening to incoming packets
        threading.Thread(target=self.listen_for_packets, daemon=True).start()

    def send_packet(self, packet, dest_ip, dest_port):
        # Send a UDP packet to another router
        self.socket.sendto(json.dumps(packet).encode(), (dest_ip, dest_port))

    def listen_for_packets(self):
        # Listen for incoming UDP packets
        while True:
            data, addr = self.socket.recvfrom(1024)
            packet = json.loads(data.decode())
            self.handle_packet(packet, addr)

    def handle_packet(self, packet, addr):
        # Handle an incoming packet
        print(f"Received packet from {addr}: {packet}")
        # Here you would add code to handle different OSPF message types

    def add_connection(self, neighbor_router, link_cost):
        # Neighbor is an instance of OSPFRouter
        link_state_id = f"{self.router_id}-{neighbor_router.router_id}"
        self.connections[neighbor_router.router_id] = {'router': neighbor_router, 'link_state_id': link_state_id,
                                                       'link_cost': link_cost}

    def generate_lsa(self):
        self.last_message_number += 1
        sequence_number = int(f"{self.router_id}{self.last_message_number:02}")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for neighbor_id, data in self.connections.items():
            lsa = LSA(data['link_state_id'], sequence_number, self.router_id, data['link_cost'], timestamp)
            self.lsdb[data['link_state_id']] = lsa
            # Send the generated LSA to all neighbors
            self.forward_lsa(lsa)

    def forward_lsa(self, lsa):
        link_state_id = lsa.link_state_id

        if link_state_id not in self.forwarded_lsas:
            self.forwarded_lsas.add(link_state_id)
            for neighbor_id, data in self.connections.items():
                neighbor_router = data['router']
                neighbor_router.receive_lsa(lsa, self)  # Forward to all neighbors

    def receive_lsa(self, received_lsa, sender):
        link_state_id = received_lsa.link_state_id

        if link_state_id not in self.lsdb or received_lsa.sequence_number > self.lsdb[link_state_id].sequence_number:
            self.lsdb[link_state_id] = received_lsa
            print(f"LSA received and stored in LSDB of Router {self.router_id}: {vars(received_lsa)}")
            self.forward_lsa(received_lsa)

    def custom_dijkstra(self, graph, start):
        distances = {router_id: float('inf') for router_id in graph}
        distances[start] = 0
        previous_nodes = {router_id: None for router_id in graph}
        pq = [(0, start)]

        while pq:
            current_distance, current_router = heapq.heappop(pq)

            for neighbor, weight in graph[current_router].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_router
                    heapq.heappush(pq, (distance, neighbor))

        # Extract paths from previous_nodes
        paths = {router_id: self._extract_path(previous_nodes, start, router_id) for router_id in graph}

        return distances, paths

    def _extract_path(self, previous_nodes, start, end):
        path = []
        current = end
        while current is not None and current != start:
            path.insert(0, current)
            current = previous_nodes[current]
        if current is not None:
            path.insert(0, start)
        return path

    def build_forwarding_table(self):
        graph = {}
        for lsa in self.lsdb.values():
            source, dest = lsa.link_state_id.split('-')
            if source not in graph:
                graph[source] = {}
            graph[source][dest] = lsa.link_cost

        shortest_paths = self.custom_dijkstra(graph, self.router_id)
        return shortest_paths
