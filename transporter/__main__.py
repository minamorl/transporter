import os
import paramiko
import hashlib
import sys

from transporter.compress import is_image_compressable, compress

def setup_ssh():
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
        port=int(lkup['port']),
        key_filename=os.path.join(os.getenv('HOME'), '.ssh/id_rsa.pub')
    )
    return client


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
    return hash_from_file(filepath) + extension


def main():
    if not (len(sys.argv) > 1 and os.path.isfile(sys.argv[1])):
        print("Missing argument. Abort.")
        return 1

    filepath = os.path.expanduser(sys.argv[1])
    new_filename = generate_hashed_filename(filepath)

    remote_path = "bucket/" + new_filename
    ssh = setup_ssh()
    sftp = ssh.open_sftp()
    sftp.put(filepath, remote_path)
    sftp.close()
    print(remote_path)

    if is_image_compressable(filepath):
        remote_path_thumb = remote_path + ":thumb"
        compressed = compress(filepath)
        sftp = ssh.open_sftp()
        sftp.put(compressed.name, remote_path_thumb)
        sftp.close()
        compressed.close()
        print(remote_path_thumb)

    ssh.close()

if __name__ == "__main__":
    main()
