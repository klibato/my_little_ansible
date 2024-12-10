import logging
import argparse
from utils import load_yaml_file, create_ssh_client
from modules.apt import AptModule
from modules.copy import CopyModule
from modules.template import TemplateModule
from modules.service import ServiceModule
from modules.sysctl import SysctlModule
from modules.command import CommandModule

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - root - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

logging.getLogger("paramiko").setLevel(logging.WARNING)


def main():
    parser = argparse.ArgumentParser(description="MyLittleAnsible")
    parser.add_argument("-f", "--file", required=True, help="Fichier YAML des tâches")
    parser.add_argument("-i", "--inventory", required=True, help="Fichier YAML des hôtes")
    parser.add_argument("--dry-run", action="store_true", help="Mode Dry Run")
    args = parser.parse_args()

    todos = load_yaml_file(args.file)
    inventory = load_yaml_file(args.inventory)

    for host_name, host_config in inventory["hosts"].items():
        logger.info(f"Connexion à l'hôte {host_name} ({host_config['ssh_address']})")
        host_summary = {"ok": 0, "changed": 0, "fail": 0}  # Initialisation du résumé

        try:
            ssh_client = create_ssh_client(
                host=host_config["ssh_address"],
                port=host_config["ssh_port"],
                username=host_config.get("ssh_user"),
                password=host_config.get("ssh_password"),
                key_file=host_config.get("ssh_key_file"),
            )
        except Exception as e:
            logger.error(f"Impossible de se connecter à {host_name} : {e}")
            continue

        task_counter = 1  
        for task in todos:
            module_name = task.get("module")
            params = task.get("params", {})

            if not module_name:
                logger.warning(f"[{task_counter}] Tâche sans module spécifié, ignorée.")
                task_counter += 1
                continue

            formatted_params = ", ".join(f"{k}={v}" for k, v in params.items())
            logger.info(f"[{task_counter}] host={host_name} op={module_name} {formatted_params}")

            if args.dry_run:
                logger.info(f"[{task_counter}] host={host_name} op={module_name} Dry Run: {formatted_params}")
                task_counter += 1
                continue

            try:
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
                    task_counter += 1
                    continue

                task_status = module.process(ssh_client)
                if task_status == "OK":
                    host_summary["ok"] += 1
                elif task_status == "CHANGED":
                    host_summary["changed"] += 1
                logger.info(f"[{task_counter}] host={host_name} op={module_name} status={task_status}")
            except Exception as e:
                host_summary["fail"] += 1
                logger.error(f"[{task_counter}] host={host_name} op={module_name} Erreur: {str(e)[:200]}")

            task_counter += 1

        ssh_client.close()
        logger.info(f"host={host_name} ok={host_summary['ok']} changed={host_summary['changed']} fail={host_summary['fail']}")


if __name__ == "__main__":
    main()
