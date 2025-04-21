from setuptools import setup, find_packages

setup(
    name='cmd_logger',
    version='0.1',
    packages=find_packages(),  # This finds the cmd_logger package
    install_requires=[
        'click',  # Add any dependencies here
    ],
    entry_points={
        'console_scripts': [
            'cmdlog=cmd_logger.main:main',  # This sets the entry point
        ],
    },
)