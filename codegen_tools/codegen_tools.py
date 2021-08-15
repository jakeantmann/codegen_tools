"""Main module."""

import sys
import subprocess
import os
import os.path
import inspect

#name = sys.argv[1]

class JavaError(Exception):
    pass

    
def type_check(name: str, my_type: type):
    # Get obj    
    frame=inspect.currentframe()
    obj = frame.f_back.f_locals[name]
    del frame
        
    # Check the type of the object
    if not isinstance(obj, my_type):
        raise TypeError(f'{name} should be {my_type}, was {type(obj)}')
        
    return obj
    
def name_from_yaml(yaml):
    return yaml.split('/')[-1].split('.')[0]

class Generator:
    def __init__(self, directory:str ='.'):
        self.directory = type_check('directory', str)

        # Check input_dir exists    
        if not os.path.isdir(self.directory):
            raise FileNotFoundError(f"{self.directory} does not exist.")
    
        self.input_dir = f"{self.directory}/yamls"
        self.output_dir = f"{self.directory}/apis"            

        self.command_map = {
                                "client": "python",
                                "server": "python-flask"
                            }                            

    def _generate_command(self, type_to_generate, yaml):
        type_text = self.command_map[type_to_generate]
        name = name_from_yaml(yaml)
        return f"openapi-generator generate -i {self.input_dir}/{yaml} -g {type_text} --package-name {name} --output {self.output_dir}/{name}-{type_to_generate}"

    def _build(self, build_type: str, yaml: str):
        build_type = type_check('build_type', str).lower()
        type_check('yaml', str)
        if build_type not in ('server', 'client'):
            raise ValueError(f"{buid_type} should be either 'server' or 'client'; was {build_type}")

        command = self._generate_command(build_type, yaml)
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            raise JavaError(error)
        print(f"{name_from_yaml(yaml)}-{build_type} built.")

    def _server(self, yaml):
        self._build("server", yaml)

    def _client(self, yaml):
        self._build("client", yaml)
        
    def build_all(self):
        for yaml in os.listdir(self.input_dir):
            self._server(yaml)
            self._client(yaml)
        

