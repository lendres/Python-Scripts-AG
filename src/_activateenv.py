#!/usr/bin/env python3
# Obtained from https://github.com/agurwicz/scripts.

import os
import sys
from argparse import SUPPRESS

from _basescript import BaseScript


class ActivateEnv(BaseScript):

    @property
    def _description(self):
        return 'Activates Python environment.'

    @property
    def _variables_to_check(self):
        return ['python_environments_path', 'activate_relative_path']

    def parse_arguments(self):
        
        # Redirecting argparse's help to stderr to work with `eval` and `call`.
        help_function = self._argument_parser.print_help
        self._argument_parser.print_help = lambda: help_function(sys.stderr)

        self._argument_parser.add_argument(
            'environment_name',
            help='name of the environment to be activated',
            type=self.existing_environment
        )

        self._argument_parser.add_argument(
            '--spawn-shell',
            help=SUPPRESS,  # Argument used for internal scripts, shouldn't appear for users.
            action='store_true'
        )

        return super().parse_arguments()

    def run(self):

        activate_path = os.path.join(
            self._variables.python_environments_path,
            self._arguments.environment_name,
            self._variables.activate_relative_path
        )

        if self._is_windows:
            # Calling `activate.bat` from subprocess doesn't propagate environment to the terminal.

            if not self._arguments.spawn_shell:
                # Solving by printing to stdout, to be captured by a `call` from a batch script.
                print(activate_path, file=sys.stdout)

            else:
                # Solving by spawning a new shell that starts running `activate.bat`.
                # Exit with `exit` instead of usual `deactivate`.
                self.run_command(command='cmd', parameters=('/k', activate_path), show_output=True)

        else:
            # Can't `source` from within Python.

            if not self._arguments.spawn_shell:
                # Solving by printing to stdout, to be captured by an `eval` call from a bash script.
                print('source {}'.format(activate_path), file=sys.stdout)

            else:
                # Solving by setting `rcfile` to the activation script, but this spawns a new shell.
                # Exit with `exit` instead of usual `deactivate`.
                self.run_command(
                    command='/usr/bin/env',
                    parameters=('bash', '--rcfile', activate_path),
                    show_output=True
                )

if __name__ == '__main__':
    ActivateEnv()
