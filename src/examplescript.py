from _basescript import BaseScript
from listenvs import ListEnvs

class ExampleScript(BaseScript):

    @property
    def _description(self):
        return 'Example description.'

    @property
    def _variables_to_check(self):
        return ['python_environments_path']

    def parse_arguments(self):

        self._argument_parser.add_argument(
            'environment_name',
            help='name of the environment to run Spyder in',
            type=self.existing_environment
        )

        return super().parse_arguments()

    def run(self):
        
        print(self._arguments.environment_name)
        ListEnvs()

if __name__ == '__main__':
    ExampleScript()