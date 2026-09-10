# gtpm

A lightweight package manager for Termux — install, remove, and upgrade packages from a local file or a remote repository, with real safety checks along the way.

## Why

Termux doesn't have a simple way to install personal scripts and tools as real, trackable "packages." `gtpm` fixes that — it works like `pkg`/`apt`, but for your own stuff (or your friends'). Built from scratch as a personal project to actually understand how a package manager works under the hood, not just use one.

## Features

- `install` / `remove` / `upgrade` / `list` — the core commands you'd expect
- Installs from a local `.tar.gz` **or** a package name from a remote index
- SHA-256 checksum verification on remote downloads
- Path traversal protection — rejects unsafe paths in a package's file list
- Manifest validation — clear errors instead of crashes on bad packages
- Every install runs in an isolated temp directory, cleaned up automatically
- Zero dependencies — just Python's standard library

## Installation

```bash
git clone git@github.com:Geot125/gtpm.git
cd gtpm
./gtpm.sh
```

That's it — `gtpm` is now a real command on your system.

## Usage

```bash
gtpm install mytool              # install from the remote index
gtpm install ./mytool-1.0.0.tar.gz  # install from a local file
gtpm remove mytool
gtpm upgrade mytool
gtpm list
gtpm help
```

## Package format

A `gtpm` package is a `.tar.gz` containing a `manifest.json` and the files it installs:

```
mytool-1.0.0.tar.gz
├── manifest.json
├── bin/
│   └── mytool
└── share/
    └── mytool/
        └── data.txt
```

`manifest.json`:
```json
{
  "name": "mytool",
  "version": "1.0.0",
  "description": "A short one-line summary of what this does",
  "maintainer": "yourname",
  "arch": "all",
  "dependencies": [],
  "files": ["bin/mytool", "share/mytool/data.txt"]
}
```

Files are installed relative to Termux's `$PREFIX`.

> **Note:** the folder layout above (`bin/`, `share/`, etc.) is just an example. A package can use whatever folders and file paths make sense for it — the only requirement is that `manifest.json` keeps its required structure (`name`, `version`, `files`, etc.) and that every path listed in `files` actually exists in the package.

## Status

Personal project, actively growing. No dependency resolution yet.

## License

MIT — see [LICENSE](LICENSE).
