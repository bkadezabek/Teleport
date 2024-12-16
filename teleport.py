import argparse
import os
import json
from pathlib import Path

# Define primary and fallback storage paths
PRIMARY_ALIASES_FILE = Path("/usr/local/share/teleport/aliases.json")
FALLBACK_ALIASES_FILE = Path.home() / ".teleport/aliases.json"

# Determine the storage file to use
if PRIMARY_ALIASES_FILE.parent.is_dir() and os.access(PRIMARY_ALIASES_FILE.parent, os.W_OK):
    ALIASES_FILE = PRIMARY_ALIASES_FILE
else:
    ALIASES_FILE = FALLBACK_ALIASES_FILE
    ALIASES_FILE.parent.mkdir(parents=True, exist_ok=True)

ALIASES_FILE.touch(exist_ok=True)

# Load existing aliases


def load_aliases():
    try:
        with open(ALIASES_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

# Save aliases


def save_aliases(aliases):
    with open(ALIASES_FILE, "w") as f:
        json.dump(aliases, f, indent=4)


def add_alias(name, path):
    aliases = load_aliases()
    if not os.path.isabs(path):
        print(f"Error: Path must be absolute: {path}")
        return
    aliases[name] = path
    save_aliases(aliases)
    print(f"Successfully added alias '{name}' with path: {path}")


def delete_alias(name):
    aliases = load_aliases()
    if name in aliases:
        removed_path = aliases.pop(name)
        save_aliases(aliases)
        print(f"Successfully deleted alias '{name}' with path: {removed_path}")
    else:
        print(f"Error: Alias '{name}' not found.")


def list_aliases(verbose):
    aliases = load_aliases()
    if not aliases:
        print("No aliases found.")
        return
    for name, path in aliases.items():
        if verbose:
            print(f"Alias: {name} ->  {path}")
        else:
            print(f"{name}")


def teleport_to(name):
    aliases = load_aliases()
    if name in aliases:
        # Output the path for shell to use with `cd $(teleport name)`
        print(aliases[name])
    else:
        print(f"Error: Alias '{name}' not found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Teleport to directories via aliases.")
    parser.add_argument("-a", metavar="NAME",
                        help="Add a new alias.", type=str)
    parser.add_argument(
        "-p", metavar="PATH", help="Path for the alias (requires -a).", type=str, default=None)
    parser.add_argument("-d", metavar="NAME",
                        help="Delete an alias.", type=str)
    parser.add_argument("-l", action="store_true", help="List all aliases.")
    parser.add_argument("-v", action="store_true",
                        help="Verbose listing (use with -l).")
    parser.add_argument("name", nargs="?", help="Teleport to the alias.")

    args = parser.parse_args()

    if args.a:
        path = args.p if args.p else os.getcwd()
        add_alias(args.a, path)
    elif args.d:
        delete_alias(args.d)
    elif args.l:
        list_aliases(verbose=args.v)
    elif args.name:
        teleport_to(args.name)
    else:
        parser.print_help()
