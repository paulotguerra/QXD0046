from setuptools import setup, find_packages
  
setup(
    name='teocomp',
    version='0.1',
    description='A simple Python package for teaching Theory of Computing',
    author='Davi Romero, Paulo T. Guerra',
    author_email='daviromero@ufc.br, paulotguerra@ufc.br',
    packages=find_packages(),
    install_requires=[
        'graphviz',
    ],
)