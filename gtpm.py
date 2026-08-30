import tarfile
import shutil
import os
import json

def extract_package(tarball_path, dest=None):
    if dest is None:
        dest = os.path.expanduser("~/.gtpm/tmp/gtpm-extract")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    with tarfile.open(tarball_path, "r:gz") as tar:
        tar.extractall(dest, filter="data")
    return dest

def read_manifest(extracted_path):
    manifest_path = os.path.join(extracted_path, "manifest.json")
    with open(manifest_path, "r") as f:
        data = json.load(f)
    return data

def install_package(extracted_path, manifest):
    prefix = os.environ.get("PREFIX")
    for relative_path in manifest["files"]:
        source = os.path.join(extracted_path, relative_path)
        destination = os.path.join(prefix, relative_path)
        dest_dir = os.path.dirname(destination)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(source, destination)

if __name__ == "__main__":
    extracted_path = extract_package("mytool-1.0.0.tar.gz")
    print(f"Extraction done, check {extracted_path}")
    manifest = read_manifest(extracted_path)
    print(manifest)
    install_package(extracted_path, manifest)