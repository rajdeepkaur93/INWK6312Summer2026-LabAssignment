import yaml
import logging
from netmiko import Netmiko

# Setup Logger
logging.basicConfig(
    filename='network_automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load hosts
hosts = yaml.load(open('network.yml'), Loader=yaml.SafeLoader)

for host in hosts["hosts"]:
    try:
        logger.info(f"Connecting to {host['name']}")
        net_connect = Netmiko(
            host=host["name"],
            username=host["username"],
            password=host["password"],
            port=host["port"],
            device_type=host["type"]
        )

        output = net_connect.send_command("show ip route", use_textfsm=True)
        net_connect.disconnect()

        print("="*60)
        print(f"Routing Table for {host['name']}")
        print("="*60)
        for route in output:
            print(f"Protocol: {route['protocol']}, Network: {route['network']}, Distance: {route['distance']}, Metric: {route['metric']}")
        logger.info(f"Routing table collected from {host['name']}")

    except Exception as e:
        print(f"ERROR on {host['name']}: {e}")
        logger.error(f"ERROR on {host['name']}: {e}")
