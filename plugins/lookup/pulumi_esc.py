from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
import subprocess
import json

DOCUMENTATION = """
---
lookup: pulumi_esc
author:
  - Your Name (@driaan)
version_added: "1.0.0"
short_description: Retrieves secrets from Pulumi ESC environments.
description:
  - This lookup plugin fetches the value of a specified key from a given Pulumi ESC environment.
options:
  env:
    description:
      - The Pulumi ESC environment from which to retrieve the secret.
    required: true
    type: str
  key:
    description:
      - The key of the secret to retrieve.
    required: true
    type: str
  value_format:
    description:
      - The format in which to retrieve the secret's value.
    required: false
    type: str
    default: 'json'
  show_secrets:
    description:
      - Whether to display secrets in the output.
    required: false
    type: bool
    default: false
notes:
  - Ensure the Pulumi ESC CLI (`esc`) is installed and accessible in the system's PATH.
"""

EXAMPLES = """
- name: Retrieve a secret from Pulumi ESC
  debug:
    msg: "{{ lookup('pulumi_esc', env='my_env', key='my_secret') }}"

- name: Retrieve a secret in plain text format
  debug:
    msg: "{{ lookup('pulumi_esc', env='my_env', key='my_secret', value_format='plain') }}"

- name: Retrieve a secret and show its value
  debug:
    msg: "{{ lookup('pulumi_esc', env='my_env', key='my_secret', show_secrets=True) }}"
"""

RETURN = """
_raw:
  description:
    - The value of the specified key from the Pulumi ESC environment.
  type: str
"""


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        env = kwargs.get("env")
        key = kwargs.get("key")

        if not env or not key:
            raise AnsibleError(
                "Both 'env' and 'key' must be provided as named parameters for Pulumi ESC lookup"
            )

        value_format = kwargs.get("value_format", "json")
        show_secrets = kwargs.get("show_secrets", False)

        command = ["esc", "env", "get", env, key, "--value", value_format]
        if show_secrets:
            command.append("--show-secrets")

        try:
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            secret_value = json.loads(result.stdout)
            if secret_value is None:
                raise AnsibleError(
                    f"Key '{key}' not found in Pulumi ESC environment '{env}'"
                )
            return [secret_value]
        except subprocess.CalledProcessError as e:
            raise AnsibleError(
                f"Error fetching key '{key}' from Pulumi ESC environment '{env}': {e.stderr}"
            )
        except FileNotFoundError:
            raise AnsibleError(
                "The Pulumi ESC CLI (`esc`) is required but was not found. "
                "Ensure it is installed and available in the system's PATH."
            )
