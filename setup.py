
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='avtMonExp',
    version='0.1.0',
    description='The project on Python 3 for searching experts of a given domain in Twitter',
    long_description=readme,
    author='A.V.T. Software (Andrei Tolstikov, Vita Tolstikova)',
    author_email='support@software.avt.dn.ua',
    url='https://github.com/SP-Vita-Tolstikova/avtMonExp',
    license=license,
    packages=find_packages()
)
