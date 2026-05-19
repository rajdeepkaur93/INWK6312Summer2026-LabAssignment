import yaml
import logging
from jinja2 import Environment, FileSystemLoader
from netmiko import Netmiko

# Setup Logger
logging.basicConfig(
    filename='network_automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load hosts from YAML
hosts = yaml.load(open('network.yml'), Loader=yaml.SafeLoader)

# Setup Jinja2
env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, autoescape=True)
template = env.get_template('router_config.j2')

# Push config to each device
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
        print(f"Logged into {host['name']} successfully")
        logger.info(f"Logged into {host['name']} successfully")

        # Render config for this host
        config = template.render(host=host)

        # Push config
        output = net_connect.send_config_set(config.split("\n"))
        print(f"Pushed config to {host['name']} successfully")
        logger.info(f"Pushed config to {host['name']} successfully")

        net_connect.disconnect()

    except Exception as e:
        print(f"ERROR on {host['name']}: {e}")
        logger.error(f"ERROR on {host['name']}: {e}")

print("Done!")
logger.info("All devices configured successfully!")
