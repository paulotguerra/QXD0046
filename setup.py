from setuptools import setup
  
setup(
    name='teocomp',
    version='0.1',
    description='A simple Python package for teaching Theory of Computing',
    author='Davi Romero, Paulo T. Guerra',
    author_email='daviromero@ufc.br, paulotguerra@ufc.br',
    packages=['teocomp'],
    install_requires=[
        'graphviz',
    ],
)