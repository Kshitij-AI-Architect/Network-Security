"""The setup.py file is essential part of packaging and distributing Python projects. 
    It is used by setuptools to define the configuration of the project, 
    such as the metadata, dependencies and more
"""

from setuptools import setup, find_packages
from typing import List

def get_requirements()-> List[str]:
    """Reads the requirements.txt file and returns a list of dependencies."""
    requirement_list : List[str] = []
    try:
        with open("requirements.txt", "r") as file:
            #Read lines from the file
            lines = file.readlines()
            #Process each line
            for line in lines:
                #Strip whitespace and newline characters
                requirement=line.strip()
                #Ignore empty lines and -e .
                if requirement and requirement!= "-e .":
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")
    return requirement_list

print(get_requirements())

setup(
    name="ml_network_security",
    version="0.0.1",
    author="Kshitij",
    author_email="kshitijsaxena734@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)