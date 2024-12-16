# Teleport (tp)

tp is a Python-based utility that lets you create and manage aliases for directories, enabling quick navigation between them in your terminal.

Teleport (navigate) to directories using their alias. You can Add and Delete aliases and also List all stored aliases.


## Installation

To use tp, place the script in your system's PATH and ensure it is executable:

chmod +x teleport.py
sudo mv teleport.py /usr/local/bin/tp

NYI: Brew support and other package managers... Will be implemented soon :)


## Usage:

### Add an alias 'angular-project' for the current directory

tp -a angular-project

**If you want to specify a path with the alias but are not in the directory you want to add:**

tp -a angular-project -p ~/users/user/web-projects/angular-project
Ensure the paths provided are absolute if using -p argument!

### Teleport to the directory associated with 'projects'

tp angular-project

### Delete an Alias

tp -d angular-project

### List Aliases that are currently in use

tp -l

**Verbose Listing:**
tp -l -v
tp -lv
**Output:**
Alias: angular-project -> /home/user/angular-project

## Storage

Aliases are stored in: /usr/local/share/teleport/aliases.json (if writable by the user)

cd ~/.teleport/aliases.json (fallback for non-root users)

### Notes:
Use sudo for commands if required to write to /usr/local/share/teleport/.

