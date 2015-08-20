import os
import hashlib
import sys
import clint

from transporter.compress import is_image_compressable, compress
from transporter.utils import generate_hashed_filename
from transporter.s3 import transfer

def main():
    if not (len(sys.argv) > 1 and os.path.isfile(sys.argv[1])):
        print("Missing argument. Abort.")
        return 1

    filepath = os.path.expanduser(sys.argv[1])
    new_filename = generate_hashed_filename(filepath)

    remote_path = 'bucket/' + new_filename
    bucket = os.environ.get("S3_TRANSPORTER_BUCKET")
    if bucket is None:
        print("S3_TRANSPORTER_BUCKET is empty. Abort")
        return 1
        
    transfer(filepath, bucket, remote_path)
    print(remote_path)

    if is_image_compressable(filepath):
        remote_path_thumb = remote_path + ":thumb"
        compressed = compress(filepath)
        transfer(compressed.name, bucket, remote_path_thumb)
        print(remote_path_thumb)

if __name__ == "__main__":
    main()
