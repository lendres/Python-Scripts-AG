#!/usr/bin/env python3
# Obtained from https://github.com/agurwicz/scripts.

import os
import sys

from _basescript import BaseScript


class StartSpyder(BaseScript):

    @property
    def _description(self):
        return 'Starts Spyder within the given environment.'

    @property
    def _variables_to_check(self):
        return ['python_environments_path']

    def parse_arguments(self):
        
        # Redirecting argparse's help to stderr to work with `eval` and `call`.
        help_function = self._argument_parser.print_help
        self._argument_parser.print_help = lambda: help_function(sys.stderr)

        self._argument_parser.add_argument(
            'environment_name',
            help='name of the environment to be activated',
            type=self.existing_environment
        )

        return super().parse_arguments()
    
    def _get_env_path(self):
        return os.path.join(
            self._variables.python_environments_path,
            self._arguments.environment_name
        )
    
    def _get_spyder_path(self):
        spyder_path = self._get_env_path()
        
        if self._is_windows:
            spyder_path = os.path.join(spyder_path, 'Scripts', 'spyder.exe')
        else:
            spyder_path = os.path.join(spyder_path, 'bin', 'spyder')
            
        return spyder_path

    @staticmethod
    def _check_spyder_installed(spyder_path):
        if not os.path.exists(spyder_path):
            raise Exception('Spyder must be installed in the environment.')
    
    def _launch_spyder(self, spyder_path, spyder_args=None):
        if spyder_args is None:
            spyder_args = []
            
        # For Spyder to have separate PYTHONPATH management, it needs a separate configuration file
        # for each environment. It cannot be done automatically by Spyder so we have to pass an argument
        # to tell Spyder where to retrieve/store its configuration file.
        configFile = os.path.join(self._get_env_path(), '.spyder-config')
        args = ['--conf-dir', configFile] + spyder_args
        
        self.open_command(
            command=spyder_path,
            parameters=args
        )

    def run(self):
        # This checks that the environment argument was passed and that it already exists.
        if self.existing_environment(environment_name=self._arguments.environment_name) is None:
            raise Exception('Must pass environment to activate.')

        spyder_path = self._get_spyder_path()
        self._check_spyder_installed(spyder_path=spyder_path)
        self._launch_spyder(spyder_path=spyder_path)


if __name__ == '__main__':
    StartSpyder()
