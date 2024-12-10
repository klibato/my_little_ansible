import yaml
import paramiko

def load_yaml_file(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def create_ssh_client(host, port, username, password=None, key_file=None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if key_file:
        ssh.connect(host, port=port, username=username, key_filename=key_file)
    else:
        ssh.connect(host, port=port, username=username, password=password)
    return ssh
