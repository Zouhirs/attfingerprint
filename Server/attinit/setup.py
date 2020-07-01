from setuptools import setup
setup(
    name = 'attinit',
    version = '0.1.0',
    packages = ['attinit'],
    entry_points = {
        'console_scripts': [
            'attinit = attinit.__main__:main'
        ]
    })
