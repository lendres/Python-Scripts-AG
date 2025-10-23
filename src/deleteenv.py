#!/usr/bin/env python3
# Obtained from https://github.com/agurwicz/scripts.

import os
from shutil import rmtree

from _basescript import BaseScript


class DeleteEnv(BaseScript):

    @property
    def _description(self):
        return 'Deletes Python environment.'

    @property
    def _variables_to_check(self):
        return ['python_environments_path']

    def parse_arguments(self):

        self._argument_parser.add_argument(
            'environment_name',
            help='name of the environment to be deleted',
            type=self.existing_environment
        )

        return super().parse_arguments()

    def run(self):
        
        rmtree(os.path.join(self._variables.python_environments_path, self._arguments.environment_name))


if __name__ == '__main__':
    DeleteEnv()
