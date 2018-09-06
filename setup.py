from setuptools import setup

# read the contents of README.md
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dcim_fau',
    version='0.1',
    packages=['dcim_fau'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'scaffold=dcim.command_line:bootstrap',
            'run=dcim.command_line:run',
        ]
    },
    long_description = long_description,
    long_description_content_type = 'text/markdown'
)

