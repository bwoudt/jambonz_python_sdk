# setup.py
from setuptools import setup, find_packages

setup(
    name='jambonz',
    version='0.1.0',
    description='A Python SDK for interacting with Jambonz CPaaS',
    author='Bjorn Woudt',
    author_email='bjorn@wiwomedia.nl',
    url='https://github.com/bwoudt/jambonz_python_sdk',
    packages=find_packages(),
    install_requires=[
        'quart==0.17.0',
        'requests==2.31.0',
        'python-dotenv==1.0.0',
        'websockets==11.0.3',
        'werkzeug==2.0.3',
        'aiohttp==3.10.10'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
