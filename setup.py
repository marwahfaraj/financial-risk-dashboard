'''
The setup.py file is an essential part of packaging and
distributing Python projects. It is used by setuptools
(or distutils in older Python versions) to define the configuration
of your project, such as its metadata, dependencies, and more.
'''

from setuptools import find_packages, setup
from typing import List


def get_requirements() -> List[str]:
    """
    This function will return a list of requirements
    """
    requirement_list: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            # Read lines from the file
            lines = file.readlines()
            # Process each line
            for line in lines:
                requirement = line.strip()
                # Ignore empty lines and "-e ."
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_list


setup(
    name="financial-risk-dashboard",
    version="1.0.0",
    author="Archana Suresh Patil, Marwah Faraj",
    description="A financial risk dashboard with ML models and Docker integration",
    packages=find_packages(),
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    project_urls={
        "Source": "https://github.com/marwahfaraj/financial-risk-dashboard",
    },
)
