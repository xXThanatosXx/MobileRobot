from setuptools import find_packages
from setuptools import setup

setup(
    name='difrobot_controller',
    version='0.0.0',
    packages=find_packages(
        include=('difrobot_controller', 'difrobot_controller.*')),
)
