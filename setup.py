from setuptools import setup, find_packages

setup(
    name='django-occupied',
    version='2.0.0',
    author='Colin Barnwell',
    description='Adds db-locks to executables.',
    long_description=open('README.md').read(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[]
)
