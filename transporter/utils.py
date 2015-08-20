import os
import paramiko
import hashlib
import sys
import boto3


def generate_hashed_filename(filepath):
    def hash_from_file(filepath):
        with open(filepath, "rb") as f:
            data = f.read()
            sha1h = hashlib.sha1()
            sha1h.update(data)
            return sha1h.hexdigest()

    def get_extension(filename):
        return os.path.splitext(filename)[1]

    filename = os.path.basename(filepath)
    extension = get_extension(filepath)
    return hash_from_file(filepath) + extension
