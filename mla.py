import logging
import argparse
from utils import load_yaml_file, create_ssh_client
from modules.apt import AptModule
from modules.copy import CopyModule
from modules.template import TemplateModule
from modules.service import ServiceModule
from modules.sysctl import SysctlModule
from modules.command import CommandModule

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="MyLittleAnsible")
    parser.add_argument("-f", "--file", required=True, help="Fichier YAML des tâches")
    parser.add_argument("-i", "--inventory", required=True, help="Fichier YAML des hôtes")
    parser.add_argument("--dry-run", action="store_true", help="Mode Dry Run")
    args = parser.parse_args()

    todos = load_yaml_file(args.file)
    inventory = load_yaml_file(args.inventory)

    for host_name, host_config in inventory['hosts'].items():
        logger.info(f"Connexion à l'hôte {host_name} ({host_config['ssh_address']})")
        ssh_client = create_ssh_client(
            host=host_config['ssh_address'],
            port=host_config['ssh_port'],
            username=host_config.get('ssh_user'),
            password=host_config.get('ssh_password'),
            key_file=host_config.get('ssh_key_file')
        )

        for task in todos:
            module_name = task.get("module")
            params = task.get("params", {})

            if not module_name:
                logger.warning("Tâche sans module spécifié, ignorée.")
                continue

            logger.info(f"Exécution du module {module_name} avec les paramètres {params}")

            if module_name == "apt":
                module = AptModule(params)
            elif module_name == "copy":
                module = CopyModule(params)
            elif module_name == "template":
                module = TemplateModule(params)
            elif module_name == "service":
                module = ServiceModule(params)
            elif module_name == "sysctl":
                module = SysctlModule(params)
            elif module_name == "command":
                module = CommandModule(params)
            else:
                logger.error(f"Module inconnu : {module_name}")
                continue

            if args.dry_run:
                logger.info(f"Dry Run : commande qui aurait été exécutée : {module}")
            else:
                try:
                    module.process(ssh_client)
                except Exception as e:
                    logger.error(f"Erreur lors de l'exécution du module {module_name}: {e}")

        ssh_client.close()
        logger.info(f"Déconnexion de l'hôte {host_name}")

if __name__ == "__main__":
    main()
