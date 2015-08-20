from setuptools import setup

setup(
    name='transporter',
    version='0.4.1',
    packages=['transporter'],
    entry_points={
            'console_scripts': ['transporter = transporter.__main__:main']
    },
    author='minamorl',
    author_email='minamorl@users.noreply.github.com',
    install_requires=[
        'boto3',
        'pillow',
    ],
)
