from setuptools import find_packages
from setuptools import setup

setup(
    name='difrobot_firmware',
    version='0.0.0',
    packages=find_packages(
        include=('difrobot_firmware', 'difrobot_firmware.*')),
)
