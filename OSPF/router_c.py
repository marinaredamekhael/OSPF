from ospf_router import OSPFRouter
import threading
import json
import socket

# Router C's IP and port configuration
ROUTER_C_IP = "192.168.1.3"
ROUTER_C_PORT = 6666

router_C = OSPFRouter("30", ROUTER_C_IP, ROUTER_C_PORT)

def listen_for_messages(router):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((router.ip_address, router.port))
        while True:
            data, address = sock.recvfrom(4096)
            message = json.loads(data.decode())
            print(f"Router C received message from {address}: {message}")

threading.Thread(target=listen_for_messages, args=(router_C,), daemon=True).start()

# Keep the thread alive
threading.Event().wait()
