import json

from database import save_interface_status
from router_client import get_interfaces


def callback(ch, method, props, body):
    job = json.loads(body.decode())
    router_ip = job["ip"]
    router_username = job["username"]
    router_password = job["password"]

    print(f"Received job for router {router_ip}", flush=True)

    try:
        output = get_interfaces(router_ip, router_username, router_password)
        save_interface_status(router_ip, output)
        print(f"Saved : {router_ip}")
    except Exception as e:
        print(f" Error: {e}")
