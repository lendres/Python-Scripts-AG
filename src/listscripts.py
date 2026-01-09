#!/usr/bin/env python3
# Obtained from https://github.com/agurwicz/scripts.

from pathlib import Path

from _basescript import BaseScript


class ListScripts(BaseScript):

    @property
    def _description(self):
        return 'Lists scripts available.'

    @property
    def _variables_to_check(self):
        return []

    def parse_arguments(self):
        return super().parse_arguments()

    def run(self):

        for script_path in Path(__file__).parent.iterdir():

            if (
                script_path.is_file()
                and not script_path.name.startswith(('.', '_'))
                and not (self._is_windows and script_path.suffix == '.sh')
                and not (not self._is_windows and script_path.suffix == '.bat')
                and not script_path.suffix == '.xml'
                and not script_path.suffix == '.template'
            ):

                print(script_path.with_suffix('').name)


if __name__ == '__main__':
    ListScripts()
