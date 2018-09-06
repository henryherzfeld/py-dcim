from setuptools import setup

setup(
    version='0.1',
    ...
    include_package_data=True,
    entry_points = {
        ...
        'console_scripts': ['scaffold=dcim.command_line:bootstrap'],
        'console_scripts': ['run=dcim.command_line:run'],
        ...
    }
    ...
)

