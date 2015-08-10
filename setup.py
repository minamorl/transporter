from setuptools import setup

setup (
        name='transporter',
        version='0.1.0',
        packages=['transporter'],
        entry_points={
            'console_scripts': ['transporter = transporter.__main__:main']
            },
        )
