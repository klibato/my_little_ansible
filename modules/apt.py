from modules import BaseModule
import logging

logger = logging.getLogger(__name__)

class AptModule(BaseModule):
    def process(self, ssh_client):
        package = self.params.get("name")
        state = self.params.get("state", "present")

        if state == "present":
            command = f"sudo apt-get install -y {package}"
        elif state == "absent":
            command = f"sudo apt-get remove -y {package}"
        else:
            logger.error(f"Invalid state: {state}")
            return

        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            logger.error(f"Error installing package {package}: {error}")
        else:
            logger.info(f"Package {package} processed: {output}")
