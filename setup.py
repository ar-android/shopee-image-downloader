from setuptools import setup

setup(
    name = 'sopi',
    version = '0.1.0',
    packages = ['sopi'],
    entry_points = {
        'console_scripts': [
            'sopi-dl = sopi.__init__:run'
        ]
    })