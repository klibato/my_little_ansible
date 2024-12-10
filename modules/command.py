from modules import BaseModule
import logging

logger = logging.getLogger(__name__)

class CommandModule(BaseModule):
    def process(self, ssh_client):
        command = self.params.get("command")
        shell = self.params.get("shell", "/bin/bash")

        if not command:
            logger.error("Missing 'command' in parameters")
            return

        full_command = f"{shell} -c '{command}'"
        stdin, stdout, stderr = ssh_client.exec_command(full_command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            logger.error(f"Error executing command: {error}")
        else:
            logger.info(f"Command executed successfully: {output}")
