from ospf_router import OSPFRouter
import threading
import json
import socket

# Router B's IP and port configuration
ROUTER_B_IP = "192.168.1.2"
ROUTER_B_PORT = 5555

router_B = OSPFRouter("20", ROUTER_B_IP, ROUTER_B_PORT)

def listen_for_messages(router):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((router.ip_address, router.port))
        while True:
            data, address = sock.recvfrom(4096)
            message = json.loads(data.decode())
            print(f"Router B received message from {address}: {message}")

threading.Thread(target=listen_for_messages, args=(router_B,), daemon=True).start()

# Keep the thread alive
threading.Event().wait()
