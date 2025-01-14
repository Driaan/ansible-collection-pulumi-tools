# Pulumi ESC Lookup Plugin

The `pulumi_esc` lookup plugin enables Ansible to retrieve secrets or configuration values from a Pulumi ESC environment securely. This plugin is ideal for managing sensitive data like API keys, database credentials, or configuration settings stored in Pulumi ESC.

---

## Prerequisites

Before using this plugin, ensure the following:

- **Pulumi ESC CLI**:
  - The `esc` CLI is installed and available in the system's PATH.
  - Refer to the [Pulumi ESC documentation](https://www.pulumi.com/docs) for installation and configuration instructions.

- **Pulumi Environment Configuration**:
  - The Pulumi environment (`env`) must be properly configured with the required keys and values.

---

## Parameters

| Parameter      | Required | Default | Description                                                  |
| -------------- | -------- | ------- | ------------------------------------------------------------ |
| `env`          | Yes      | None    | The Pulumi environment name.                                 |
| `key`          | Yes      | None    | The key to retrieve from the environment.                    |
| `value_format` | No       | `json`  | The output format for the value (`json`, `yaml`, etc.).      |
| `show_secrets` | No       | `False` | Whether to include the `--show-secrets` flag in the command. |

---

## Usage Example

Here’s an example playbook demonstrating how to use the `pulumi_esc` lookup plugin:

### Playbook Example
```yaml
- name: Retrieve a secret from Pulumi ESC
  hosts: localhost
  gather_facts: false
  vars:
    pulumi_env: "production"
    pulumi_key: "db_password"
    pulumi_value_format: "json"

  tasks:
    - name: Fetch secret from Pulumi ESC
      debug:
        msg: >
          "{{ lookup('driaan.pulumi_tools.pulumi_esc', 
                     env=pulumi_env, 
                     key=pulumi_key, 
                     value_format=pulumi_value_format, 
                     show_secrets=True) }}"

