import tarfile
import shutil
import os

def extract_package(tarball_path, dest=None):
    if dest is None:
        dest = os.path.expanduser("~/.gtpm/tmp/gtpm-extract")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    with tarfile.open(tarball_path, "r:gz") as tar:
        tar.extractall(dest)
    return dest

if __name__ == "__main__":
    extracted_path = extract_package("mytool-1.0.0.tar.gz")
    print(f"Extraction done, check {extracted_path}")