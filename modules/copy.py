from modules import BaseModule
import logging
import os
import hashlib

logger = logging.getLogger(__name__)

class CopyModule(BaseModule):
    def process(self, ssh_client):
        src = self.params.get("src")
        dest = self.params.get("dest")
        backup = self.params.get("backup", False)

        try:
            sftp = ssh_client.open_sftp()

            if self._file_exists(sftp, dest):
                if self._files_are_identical(sftp, src, dest):
                    logger.info(f"Le fichier {dest} est déjà à jour, aucune action nécessaire.")
                    sftp.close()
                    return "OK"
                elif backup:
                    backup_path = f"{dest}.backup"
                    sftp.rename(dest, backup_path)
                    logger.info(f"Backup créé pour {dest}")

            sftp.put(src, dest)
            logger.info(f"Fichier {src} copié vers {dest}")
            sftp.close()
            return "CHANGED"
        except FileNotFoundError:
            logger.error(f"Fichier source introuvable : {src}")
            return "FAIL"
        except PermissionError:
            logger.error(f"Permission refusée pour copier {src} vers {dest}")
            return "FAIL"
        except Exception as e:
            logger.error(f"Erreur lors de la copie : {e}")
            return "FAIL"

    def _file_exists(self, sftp, path):
        try:
            sftp.stat(path)
            return True
        except FileNotFoundError:
            return False

    def _files_are_identical(self, sftp, src, dest):
        try:
            with open(src, "rb") as src_file:
                src_hash = hashlib.md5(src_file.read()).hexdigest()
            with sftp.open(dest, "rb") as dest_file:
                dest_hash = hashlib.md5(dest_file.read()).hexdigest()
            return src_hash == dest_hash
        except Exception as e:
            logger.error(f"Erreur lors de la comparaison des fichiers {src} et {dest} : {e}")
            return False
