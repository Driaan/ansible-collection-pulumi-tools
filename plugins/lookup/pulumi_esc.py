from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
import subprocess
import json


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        # Ensure required arguments are passed as named parameters
        env = kwargs.get("env")
        key = kwargs.get("key")

        if not env or not key:
            raise AnsibleError(
                "Both 'env' and 'key' must be provided as named parameters for Pulumi ESC lookup"
            )

        # Optional arguments with opinionated default values
        value_format = kwargs.get("value_format", "json")
        show_secrets = kwargs.get("show_secrets", False)

        # Build the esc command
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