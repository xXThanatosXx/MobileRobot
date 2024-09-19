from setuptools import find_packages
from setuptools import setup

setup(
    name='difrobot_msgs',
    version='0.0.0',
    packages=find_packages(
        include=('difrobot_msgs', 'difrobot_msgs.*')),
)
