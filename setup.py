from setuptools import setup, find_packages
import os.path
import io

# read contents of README.md
this_dir = os.path.abspath(os.path.dirname(__file__))
README = io.open(os.path.join(this_dir, 'README.md'), encoding='utf8').read()

setup(name='dcim_fau',
      version='1.1a',
      long_description=README,
      long_description_content_type='text/markdown',
      author='Henry Herzfeld',
      author_email='herzfeld2@gmail.com',
      keywords=['dcim', 'fau'],
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'pyyaml',
          'pysnmp',
          'redis',
          'walrus',
          'pytest',
      ],
      python_requires=">=3.4",
      include_package_data=True,
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'test=dcim.command_line:test',
              'run=dcim.command_line:run',
              ]
          }
      )

