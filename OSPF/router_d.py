from ospf_router import OSPFRouter
import threading
import json
import socket

# Router D's IP and port configuration
ROUTER_D_IP = "192.168.1.4"
ROUTER_D_PORT = 7777

router_D = OSPFRouter("40", ROUTER_D_IP, ROUTER_D_PORT)

def listen_for_messages(router):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((router.ip_address, router.port))
        while True:
            data, address = sock.recvfrom(4096)
            message = json.loads(data.decode())
            print(f"Router D received message from {address}: {message}")

threading.Thread(target=listen_for_messages, args=(router_D,), daemon=True).start()

# Keep the thread alive
threading.Event().wait()
