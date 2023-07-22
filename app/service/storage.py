import os


def get_folder_size(path: str = '.'):
    """Return the size of a given folder, unit MB"""
    total = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            fp = os.path.join(root, file)
            if not os.path.islink(fp):
                total += os.path.getsize(fp)
    return total / (1024 * 1024)
