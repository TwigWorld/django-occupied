from setuptools import find_packages
from setuptools import setup

setup(
    name="django-occupied",
    version="2.0.0",
    author="Colin Barnwell",
    description="Adds db-locks to executables.",
    long_description=open("README.md").read(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    extras_require={
        "testing": [
            "black",
            "isort",
            "check_pdb_hook",
            "pre-commit",
            "pytest",
            "pytest-django",
        ]
    },
)
