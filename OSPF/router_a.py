from ospf_router import OSPFRouter
import threading
import json
import socket

router_A = OSPFRouter("10", "192.168.1.1", 4444)
router_A.start()

# Function to send a message to another router
def send_message_to(router, message, destination_ip, destination_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(json.dumps(message).encode(), (destination_ip, destination_port))

# Function to listen for incoming messages
def listen_for_messages(router):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((router.ip_address, router.port))
        while True:
            data, address = sock.recvfrom(4096)
            message = json.loads(data.decode())
            print(f"Router A received message from {address}: {message}")

# Start a thread to listen for messages
threading.Thread(target=listen_for_messages, args=(router_A,), daemon=True).start()

neighbors = [("192.168.1.2", 5555), ("192.168.1.3", 6666), ("192.168.1.4", 7777)]
for ip, port in neighbors:
    send_message_to(router_A, {'type': message, 'sender': '10'}, ip, port)

# Keep the main thread alive
threading.Event().wait()
