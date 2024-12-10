MyLittleAnsible - README
## Description
MyLittleAnsible est un outil d'automatisation inspiré d'Ansible. Il permet
d'exécuter des tâches déclarées dans un fichier YAML (`todos.yml`) sur des
hôtes distants définis dans un fichier d'inventaire (`inventory.yml`).
Cet outil est conçu pour être minimaliste, extensible, et compatible avec des
cas d'utilisation simples, comme la gestion de paquets, la copie de fichiers, et
l'exécution de commandes.
## Fonctionnalités
- **Installation de paquets APT (`apt`)**
- **Copie de fichiers et gestion des backups (`copy`)**
- **Génération de fichiers à partir de templates Jinja2 (`template`)**
- **Gestion des services systemd (`service`)**
- **Modification des paramètres du kernel (`sysctl`)**
- **Exécution de commandes shell arbitraires (`command`)**
## Prérequis
- **Python 3.8+**
- Bibliothèques Python nécessaires (installées via `requirements.txt`) :
 - `paramiko`
 - `pyyaml`
 - `jinja2`
 - `click`
## Installation
1. Clonez le dépôt :
 ```bash
 git clone https://github.com/<utilisateur>/my_little_ansible.git
 cd my_little_ansible
 ```
2. Créez et activez un environnement virtuel Python :
 ```bash
 python3 -m venv mla_env
 source mla_env/bin/activate
 ```
3. Installez les dépendances :
 ```bash
 pip install -r requirements.txt
 ```
## Utilisation
### Exemple de commande
```bash
python mla.py -f todos.yml -i inventory.yml
```
- `-f` : Spécifie le fichier YAML contenant les tâches à exécuter.
- `-i` : Spécifie le fichier YAML contenant l'inventaire des hôtes distants.
- `--dry-run` : Affiche les actions qui seraient exécutées sans modifier les hôtes.
### Exemple de fichier `todos.yml`
```yaml
- module: apt
 params:
 name: nginx
 state: present
- module: copy
 params:
 src: ./testfile.txt
 dest: /tmp/testfile.txt
 backup: true
- module: command
 params:
 command: echo "Hello, World!" > /tmp/hello_world.txt
 shell: /bin/bash
```
### Exemple de fichier `inventory.yml`
```yaml
hosts:
 localhost:
 ssh_address: your_adress
 ssh_port: uour_port
 ssh_user: your_user
 ssh_password: your_password
```
### Résultat attendu
```plaintext
2024-12-10 16:13:00,132 - root - INFO - Fichier ./testfile.txt copié vers
/tmp/testfile.txt
2024-12-10 16:13:00,132 - root - INFO - [3] host=localhost op=copy
status=CHANGED
2024-12-10 16:13:00,132 - root - INFO - host=localhost ok=1 changed=1 fail=0
```
## Idempotence
Le programme est conçu pour être idempotent. Par exemple :
- Si un paquet est déjà installé, il ne sera pas réinstallé.
- Si un fichier est déjà à jour, il ne sera pas recopié.
## Contribuer
Les contributions sont les bienvenues ! Pour toute amélioration ou correction
de bugs, merci de soumettre une **pull request**.
---
## Auteurs
- **Hamza El Marga** - Développeur principal
- Inspiré par l'outil Ansible
