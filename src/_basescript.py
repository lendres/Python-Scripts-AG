# Obtained from https://github.com/agurwicz/scripts.

import platform
import subprocess
import sys
import os
from abc import ABC, abstractmethod
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from pathlib import Path
from shutil import which
from xml.etree import ElementTree


class BaseScript(ABC):

    def __init__(self):

        self.__filter_exceptions()
        self._argument_parser = ArgumentParser(
            description=self._description, 
            formatter_class=ArgumentDefaultsHelpFormatter
        )
        
        self._variables = self.__get_and_check_variables(variables_to_check=self._variables_to_check)
        self._arguments = self.parse_arguments()

        self.run()

    @property
    @abstractmethod
    def _description(self):
        pass

    @property
    @abstractmethod
    def _variables_to_check(self):
        pass

    @abstractmethod
    def parse_arguments(self):
        return self._argument_parser.parse_args()

    @abstractmethod
    def run(self):
        pass
    
    @property
    def _is_windows(self):
        return 'windows' in platform.system().lower()

    @staticmethod
    def open_command(command, parameters=()):

        if not isinstance(parameters, (list, tuple)):
            parameters = [parameters]

        subprocess.Popen(args=[command]+list(parameters))

    def run_command(self, command, parameters=(), show_output=False):
        
        if not isinstance(parameters, (list, tuple)):
            parameters = [parameters]

        result = subprocess.run(
            args=[command]+list(parameters),
            capture_output=not show_output, 
            text=True,
            shell=True if self._is_windows else False
        )
        
        if not show_output:
            return result.stdout.strip()
        return None
    
    def run_script(self, script_name, parameters=(), show_output=False):

        if not isinstance(parameters, (list, tuple)):
            parameters = [parameters]

        return self.run_command(
            command=sys.executable,
            parameters=[Path(__file__).parent.joinpath(script_name).with_suffix(suffix='.py')] + list(parameters),
            show_output=show_output
        )

    def get_python_version(self, python_path):
        
        return self.run_command(
            command=python_path, 
            parameters=('-c', 'import platform; print(platform.python_version())')
        )
    
    def get_python_path(self, environment_name):
        return os.path.join(
            self._variables.python_environments_path, 
            environment_name,
            self._variables.python_relative_path
        ) if self._arguments.environment is not None else 'python'
    
    @staticmethod
    def get_script_in_path(script_name):

        script_name = Path(script_name)

        if script_name.suffix:
            extensions = [script_name.suffix]
        else:
            extensions = ['', '.sh', '.py']

        script_path = None
        for extension in extensions:

            found_path = which(
                cmd='{name}{extension}'.format(name=script_name.with_suffix(''), extension=extension)
            )

            if found_path is not None:
                script_path = found_path
                break

        if script_path is None:
            raise Exception('Script not found.')
        
        return script_path

    def open_text_file(self, file_path):

        if not self._is_windows:
            self.run_command(command='open', parameters=file_path)

        else:
            # Opening the script in the default editor for text files, ignoring file associations.
            import winreg

            def __reg_query(key, sub_key, value):

                key = winreg.OpenKey(key=key, sub_key=sub_key)
                value, _ = winreg.QueryValueEx(key, value)
                winreg.CloseKey(key)

                return value

            txt_extension = '.txt'
            try:
                program_key = __reg_query(
                    key=winreg.HKEY_CURRENT_USER,
                    sub_key=r'Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\{}\UserChoice'.format(
                        txt_extension
                    ),
                    value='ProgId'
                )

            except FileNotFoundError:
                program_key = self.run_command(command='assoc', parameters=txt_extension).split('=')[-1]

            try:
                txt_open_command = __reg_query(
                    key=winreg.HKEY_CLASSES_ROOT,
                    sub_key=r'{}\shell\open\command'.format(program_key),
                    value=''
                ).split('\"')[1]

            except FileNotFoundError:
                txt_open_command = 'notepad.exe'  # Falling back to Notepad if default program not found.

            self.open_command(command=txt_open_command, parameters=file_path)

        print('Opened {}'.format(file_path), file=sys.stdout)

    def existing_environment(self, environment_name):
        
        def __check_file(relative_path):
            return Path(self._variables.python_environments_path).joinpath(
                environment_name, 
                relative_path
            ).is_file()

        if (
            not __check_file(relative_path=self._variables.python_relative_path) 
            or not __check_file(relative_path=self._variables.activate_relative_path)
        ):
            raise Exception('Environment \"{}\" does not exist.'.format(environment_name))
        
        return environment_name
        
    def nonexistent_environment(self, environment_name):
    
        def __check_file(relative_path):
            return Path(self._variables.python_environments_path).joinpath(
                environment_name, 
                relative_path
            ).is_file()

        if (
            __check_file(relative_path=self._variables.python_relative_path) 
            or __check_file(relative_path=self._variables.activate_relative_path)
        ):
            raise Exception('Environment \"{}\" already exists.'.format(environment_name))
        
        return environment_name
    
    @staticmethod
    def __filter_exceptions():

        sys.excepthook = lambda exception_type, value, _: print(
            '{color}{type}:{reset_color} {message}'.format(
                type=exception_type.__name__,
                message=value,
                color='\033[91m',  # red
                reset_color='\033[0m'
            ),
            file=sys.stderr
        ) 

    def __get_and_check_variables(self, variables_to_check):
        
        variables_file_name = 'variables.xml'

        variables_file = ElementTree.parse(source=Path(__file__).parent.joinpath(variables_file_name))
        variables = Namespace(**variables_file.getroot().attrib)

        if self._is_windows:
            variables.python_relative_path = r'Scripts\python.exe'
            variables.python_version_relative_path = r'python.exe'
            variables.activate_relative_path = r'Scripts\activate.bat'
        else:
            variables.python_relative_path = r'bin/python'
            variables.python_version_relative_path = r'bin/python3'
            variables.activate_relative_path = r'bin/activate'

        for variable_to_check in variables_to_check:
            
            try:
                variable = getattr(variables, variable_to_check)
                if not variable:
                    raise AttributeError

            except AttributeError:
                raise Exception(
                    'Variable \"{}\" is not defined in \"{}\".'.format(variable_to_check, variables_file_name)
                )

        return variables
