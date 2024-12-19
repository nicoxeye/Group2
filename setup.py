import os

from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

version = os.getenv(
    "VERSION", "0.0.0"
)  # Fallback to '0.0.0'version = os.getenv('PACKAGE_VERSION', '0.0.0')  # Fallback to '0.0.0'



setup(
    name="nicoxeye",
    version=version,
    author="Nikola Jamrozy",
    author_email="nicoxeye@op.pl",
    description="Attendance management system for university",
    long_description=open("README.md").read(),
    url="https://github.com/nicoxeye/Group2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": ["Group2=src.cli.cli:main"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.12",
)