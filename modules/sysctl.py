from modules import BaseModule
import logging

logger = logging.getLogger(__name__)

class SysctlModule(BaseModule):
    def process(self, ssh_client):
        attribute = self.params.get("attribute")
        value = self.params.get("value")
        permanent = self.params.get("permanent", False)

        if not attribute or value is None:
            logger.error("Missing 'attribute' or 'value' in parameters")
            return

        command = f"sudo sysctl -w {attribute}={value}"
        stdin, stdout, stderr = ssh_client.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        if error:
            logger.error(f"Error setting sysctl {attribute}: {error}")
        else:
            logger.info(f"Sysctl {attribute} set to {value}: {output}")

        if permanent:
            with ssh_client.open_sftp().file("/etc/sysctl.conf", "a") as sysctl_file:
                sysctl_file.write(f"\n{attribute}={value}\n")
                logger.info(f"Persisted sysctl {attribute} to /etc/sysctl.conf")
