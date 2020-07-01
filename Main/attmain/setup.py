from setuptools import setup
setup(
    name = 'attmain',
    version = '0.1.0',
    packages = ['attmain'],
    entry_points = {
        'console_scripts': [
            'attmain = attmain.__main__:main'
        ]
    })
