from setuptools import setup
setup(
    name = 'attconfig',
    version = '0.1.0',
    packages = ['attconfig'],
    entry_points = {
        'console_scripts': [
            'attconfig = attconfig.__main__:main'
        ]
    })
