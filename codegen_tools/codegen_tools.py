"""Main module."""

import inspect
import logging
import os
import subprocess  # noqa: S404
from typing import Dict

logging.basicConfig(level=logging.INFO)


class JavaError(Exception):
    """Error for when Java misbehaves."""

    def __init__(self):
        """Empty init."""


def type_check(name: str, my_type: type):
    """Check that the type hint is followed."""
    # Get obj
    frame = inspect.currentframe()
    my_obj = frame.f_back.f_locals[name]
    del frame  # noqa: WPS420

    # Check the type of the object
    if not isinstance(my_obj, my_type):
        output_string = '{name} should be {my_type}, was {real_type}'.format(
            name=name,
            my_type=my_type,
            real_type=type(my_obj),
        )
        raise TypeError(output_string)

    return my_obj


def name_from_yaml(yaml):
    """Get a service's name from its yaml."""
    return yaml.split('/')[-1].split('.')[0]


def generate_options_string(options: Dict[str, str]) -> str:
    """Build the options string from the options dict."""
    options_list = [
        '{key} {option}'.format(key=key, option=options[key])
        for key in options
    ]
    return ' '.join(options_list)


class Generator(object):
    """Handles OpenAPI code generation."""

    def __init__(self, directory: str = '.'):
        """Set the directory value and check the directory structure."""
        self.directory = type_check('directory', str)

        # Check input_dir exists
        if not os.path.isdir(self.directory):
            output_string = '{directory} does not exist.'.format(
                directory=self.directory,
            )
            raise FileNotFoundError(output_string)

        self.input_dir = '{directory}/yamls'.format(directory=self.directory)
        self.output_dir = '{directory}/apis'.format(directory=self.directory)

        self.command_map = {
            'client': 'python',
            'server': 'python-flask',
        }

    def build_all(self):
        """Generate all the clients and servers from their yamls."""
        for yaml in os.listdir(self.input_dir):
            self._build('server', yaml)
            self._build('client', yaml)

    def _generate_command(self, type_to_generate, yaml):
        """Make an OpenAPI generate command."""
        type_text = self.command_map[type_to_generate]
        name = name_from_yaml(yaml)

        options = {
            '--input-spec': '{input_dir}/{yaml}'.format(
                input_dir=self.input_dir,
                yaml=yaml,
            ),
            '--generator-name': type_text,
            '--package-name': name,
            '--output': '{output_dir}/{name}-{type_to_generate}'.format(
                output_dir=self.output_dir,
                name=name,
                type_to_generate=type_to_generate,
            ),
        }

        generate_string = generate_options_string(options)
        return 'openapi-generator generate {generate_string}'.format(
            generate_string=generate_string,
        )

    def _build(self, build_type: str, yaml: str):
        """Build a client or server."""
        build_type = type_check('build_type', str).lower()
        type_check('yaml', str)
        if build_type not in {'server', 'client'}:
            output = (
                "{build_type} should be either 'server' or 'client'; " +
                'was {build_type}',
            ).format(build_type=build_type)
            raise ValueError(output)

        command = self._generate_command(build_type, yaml).split()
        process = subprocess.Popen(  # noqa: S603
            command, stdout=subprocess.PIPE,
        )
        _, error = process.communicate()
        if error:
            raise JavaError(error)

        logging.info(
            '{name}-{build_type} built.'.format(
                name=name_from_yaml(yaml),
                build_type=build_type,
            ),
        )
