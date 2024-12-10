from modules import BaseModule
import logging

logger = logging.getLogger(__name__)

class ServiceModule(BaseModule):
    def process(self, ssh_client):
        name = self.params.get("name")
        state = self.params.get("state")

        if not name or not state:
            logger.error("Missing 'name' or 'state' in parameters")
            return

        command = None
        if state == "started":
            command = f"sudo systemctl start {name}"
        elif state == "stopped":
            command = f"sudo systemctl stop {name}"
        elif state == "restarted":
            command = f"sudo systemctl restart {name}"
        elif state == "enabled":
            command = f"sudo systemctl enable {name}"
        elif state == "disabled":
            command = f"sudo systemctl disable {name}"
        else:
            logger.error(f"Invalid state: {state}")
            return

        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            logger.error(f"Error managing service {name}: {error}")
        else:
            logger.info(f"Service {name} {state}: {output}")
