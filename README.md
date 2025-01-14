# Pulumi Tools - Lookup Plugin

This collection provides a custom Ansible lookup plugin for securely fetching secrets from Pulumi ESC. Requires the Pulumi ESC CLI.

## Features
- Fetch secrets by environment and key.
- Configurable output formats (`json` by default).
- Optional `--show-secrets` support.

## Requirements

- Ansible 2.9 or later
- Pulumi ESC CLI installed and configured on the system running the playbook
  - The `esc` command must be available in the system's PATH.
- Python 3.6 or later

## Installation
To install this collection, run:

```bash
ansible-galaxy collection install driaan.pulumi_tools