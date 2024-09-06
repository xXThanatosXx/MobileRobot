from setuptools import find_packages, setup

package_name = 'difrobot_py_examples'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='38089172+Shadowelec1986@users.noreply.github.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simple_turtlesim_kinematics = difrobot_py_examples.simple_turtlesim_kinematics:main',
            'simple_tf_kinematics = difrobot_py_examples.simple_tf_kinematics:main',
            'simple_service_server = difrobot_py_examples.simple_service_server:main',
            'simple_service_client = difrobot_py_examples.simple_service_client:main',
        ],
    },
)
