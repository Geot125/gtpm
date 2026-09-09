import tarfile
import shutil
import os
import json
import sys

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
    if prefix is None:
        raise SystemExit("Error: PREFIX environment variable is not set. This tool must be run inside Termux.")
    for relative_path in manifest["files"]:
        if os.path.isabs(relative_path) or ".." in relative_path.split(os.sep):
            raise SystemExit(f"Error: unsafe path in manifest: {relative_path!r}")
        source = os.path.join(extracted_path, relative_path)
        destination = os.path.join(prefix, relative_path)
        dest_dir = os.path.dirname(destination)
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(source, destination)
    status = load_status()
    status[manifest["name"]] = {
        "version": manifest["version"],
        "files": manifest["files"]
    }
    save_status(status)

def validate_manifest(manifest):
    required_keys = ["name", "version", "files"]
    for key in required_keys:
        if key not in manifest:
            raise SystemExit(f"Error: manifest is missing required key '{key}'")
    if not isinstance(manifest["files"], list):
        raise SystemExit("Error: manifest 'files' must be a list")
    for item in manifest["files"]:
        if not isinstance(item, str):
            raise SystemExit(f"Error: manifest 'files' entry {item!r} is not a string")

def load_status():
    prefix = os.environ.get("PREFIX")
    if prefix is None:
        raise SystemExit("Error: PREFIX environment variable is not set. This tool must be run inside Termux.")
    status_path = os.path.join(prefix, "var", "lib", "gtpm", "status.json")
    if os.path.exists(status_path):
        with open(status_path, "r") as f:
            return json.load(f)
    else: 
        return {}

def save_status(data):
    prefix = os.environ.get("PREFIX")
    if prefix is None:
        raise SystemExit("Error: PREFIX environment variable is not set. This tool must be run inside Termux.")
    status_path = os.path.join(prefix, "var", "lib", "gtpm", "status.json")
    status_dir = os.path.dirname(status_path)
    os.makedirs(status_dir, exist_ok=True)
    with open(status_path, "w") as f:
        json.dump(data, f, indent=2)

def remove_package(name):
    prefix = os.environ.get("PREFIX")
    if prefix is None:
        raise SystemExit("Error: PREFIX environment variable is not set. This tool must be run inside Termux.")
    status = load_status()
    if name not in status:
        raise SystemExit(f"Error: package '{name}' is not installed")
    for relative_path in status[name]["files"]:
        file_path = os.path.join(prefix, relative_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    del status[name]
    save_status(status)

if __name__ == "__main__":
    command = sys.argv[1]
    if command == "install":
        tarball_path = sys.argv[2]
        extracted_path = extract_package(tarball_path)
        print(f"Extraction done, check {extracted_path}")
        manifest = read_manifest(extracted_path)
        validate_manifest(manifest)
        print(manifest)
        install_package(extracted_path, manifest)
    elif command == "list":
        status = load_status()
        for name, info in status.items():
            print(name, info["version"])
    elif command == "remove":
        name = sys.argv[2]
        remove_package(name)
        print(f"Removed {name}")
    else:
        raise SystemExit(f"Error: unknown command '{command}'")
