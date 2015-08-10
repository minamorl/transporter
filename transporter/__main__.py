import os
import paramiko
import hashlib 
from scp import SCPClient
import sys


def setup_scp():
    config_file = os.path.join(os.getenv('HOME'), '.ssh/config')
    known_host = paramiko.hostkeys.HostKeys()
    
    ssh_config = paramiko.SSHConfig()
    ssh_config.parse(open(config_file, 'r'))
    lkup = ssh_config.lookup("minamorl-com")

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        lkup['hostname'],
        port=int(lkup['port']) ,
        key_filename=os.path.join(os.getenv('HOME'), '.ssh/id_rsa.pub')
        )
    scp = SCPClient(client.get_transport())
    return scp

def hash_from_file(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
        sha1h = hashlib.sha1()
        sha1h.update(data)
        return sha1h.hexdigest()

def get_extension(filename):
    return os.path.splitext(filename)[1]

def generate_hashed_filename(filepath):
    filename = os.path.basename(filepath)
    extension = get_extension(filepath)
    return hash_from_file(filename) + extension

def main():
    scp = setup_scp()
    filepath = sys.argv[1]
    new_filename = generate_hashed_filename(filepath)

    remote_path = "bucket/" + new_filename
    scp.put(filepath, remote_path)
    scp.close()
    print(remote_path)

if __name__ == "__main__":
    main()

