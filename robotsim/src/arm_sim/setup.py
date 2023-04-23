from setuptools import setup
from glob import glob
import os

package_name = 'arm_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, glob('description/urdf/*')),
        ('share/' + package_name, glob('launch/*launch.[pxy][yma]*')),
        ('share/' + package_name, glob('worlds/*')),
        ('share/' + package_name, glob('hcode/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='markc',
    maintainer_email='markcfong561@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'follow_gcode = arm_sim.publish_pos:main', 'launch_sim = arm_sim.launch_arm:launchGazebo',
        ]
    },
    py_modules=[
        'arm_sim.gazeboControl',
    ]
)
