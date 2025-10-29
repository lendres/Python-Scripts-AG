#!/usr/bin/env python3
# Obtained from https://github.com/agurwicz/scripts.

import os
import textwrap

from _basescript import BaseScript


class InstallPackages(BaseScript):

    @property
    def _description(self):
        return 'Installs and upgrades packages in Python environment.'
    
    @property
    def _epilog(self):
        return textwrap.dedent('''
            Examples:
                isntallpackages pandas
                isntallpackages -e env "pandas, matplotlib"
        ''')

    @property
    def _variables_to_check(self):
        return ['python_environments_path', 'python_relative_path']

    def parse_arguments(self):

        self._argument_parser.add_argument(
            'packages',
            help='a string of a comma separated list of packages to install and upgrade (accepts versions with \"package==version\")',
            type=lambda packages: packages.split(',')
        )

        self._argument_parser.add_argument(
            '-e', '--environment',
            help='name of the environment to install in (default: currently active environment)',
            type=self.existing_environment
        )

        self._argument_parser.add_argument(
            '-a', '--activate',
            help='activate the environment after creation',
            action='store_true'
        )

        return super().parse_arguments()

    def run(self):
        
        if self._arguments.activate and self._arguments.environment is None:
            raise Exception("Must pass environment to activate.")

        python_path = os.path.join(
            self._variables.python_environments_path, 
            self._arguments.environment, 
            self._variables.python_relative_path
        ) if self._arguments.environment is not None else 'python'

        self.run_command(
            command=python_path,
            parameters=('-m', 'pip', 'install', '--upgrade', '--no-cache-dir', *self._arguments.packages),
            show_output=True
        )

        if self._arguments.activate:
            self.run_script(
                script_name='_activateenv', 
                parameters=(self._arguments.environment, '--spawn-shell'), 
                show_output=True
            )


if __name__ == '__main__':
    InstallPackages()
