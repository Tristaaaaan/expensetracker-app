import os


def set_file_permissions(path):
    # Set read-only permissions for the file
    os.chmod(path, 0o400)  # 0o400 is equivalent to read-only
