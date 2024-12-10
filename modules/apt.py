from modules import BaseModule
import logging

logger = logging.getLogger(__name__)

class AptModule(BaseModule):
    def process(self, ssh_client):
        package = self.params.get("name")
        state = self.params.get("state", "present")
        command = f"sudo apt-get install -y {package}" if state == "present" else f"sudo apt-get remove -y {package}"

        try:
            stdin, stdout, stderr = ssh_client.exec_command(command)
            error = stderr.read().decode()
            output = stdout.read().decode()

            if error:
                logger.error(f"Erreur avec le paquet {package}: {error[:200]}")
                return "FAIL"
            
            logger.info(f"Paquet {package} traité : {output.strip()}")
            return "CHANGED" if "installing" in output.lower() or "upgraded" in output.lower() else "OK"
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de apt : {e}")
            return "FAIL"
