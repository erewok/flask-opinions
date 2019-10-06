"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='opinions',
    version=os.getenv("OPINIONS_VERSION", "Unknown"),
    description='Flask opinions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/erewok/flask-opinions',
    author='Erik Aker',
    author_email='eraker@gmail.com',
    packages=find_packages(exclude=['test']),  # Required
    install_requires=[
        'requests',
        'Flask',
        'Jinja2',
        'gunicorn',
        'python-json-logger',
        'structlog',
        'ecological',
        'python-rapidjson'
    ],
    extras_require={
        'test': ['pytest',
                 'ipdb',
                 'coverage',
                 'pytest-cov',
                 'flake8',
                 'pytest-flake8',
                 'mypy',
                 'pytest-mypy'],
    }
)
