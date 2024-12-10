from modules import BaseModule
import logging

logger = logging.getLogger(__name__)

class CopyModule(BaseModule):
    def process(self, ssh_client):
        src = self.params.get("src")
        dest = self.params.get("dest")
        backup = self.params.get("backup", False)

        if not src or not dest:
            logger.error("Missing 'src' or 'dest' in parameters")
            return

        if backup:
            backup_cmd = f"cp -r {dest} {dest}.bak"
            stdin, stdout, stderr = ssh_client.exec_command(backup_cmd)
            logger.info(f"Backup created for {dest}: {stdout.read().decode()}")

        sftp = ssh_client.open_sftp()
        try:
            sftp.put(src, dest)
            logger.info(f"Copied {src} to {dest}")
        except Exception as e:
            logger.error(f"Failed to copy {src} to {dest}: {e}")
        finally:
            sftp.close()
