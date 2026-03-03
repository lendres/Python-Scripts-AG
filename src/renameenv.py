#!/usr/bin/env python3
# Obtained from https://github.com/agurwicz/scripts.

import os

from _basescript import BaseScript


class RenameEnv(BaseScript):

    @property
    def _description(self):
        return 'Renames Python environment.'

    @property
    def _variables_to_check(self):
        return ['python_environments_path']

    def parse_arguments(self):

        self._argument_parser.add_argument(
            'environment_name',
            help='name of the environment to be renamed',
            type=self.existing_environment
        )
        
        self._argument_parser.add_argument(
            'new_environment_name',
            help='the new environment name',
            type=self.nonexistent_environment
        )

        return super().parse_arguments()

    def run(self):
        
        old_environment_path = os.path.join(self._variables.python_environments_path, self._arguments.environment_name)
        new_environment_path = os.path.join(self._variables.python_environments_path, self._arguments.new_environment_name)
        
        try:
            os.rename(old_environment_path, new_environment_path)
        except OSError as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    RenameEnv()