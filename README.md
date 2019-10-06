# Flask Opinions

This application represents a collection of best practices and opinions cultivated over 5 years of working with Flask.

Note: this project was built with Python 3.7 (and it liberally uses F-strings).

This project includes the following features:

- Configuration management from environment variables and secret files using the [ecological](https://github.com/jmcs/ecological) package.
- Opinionated logging set-up with ability to log arbitrary kwargs using [structlog](http://www.structlog.org/en/stable/) with colored output for local
  development and JSON output to stdout in production.
  - A Dockerfile for running this in production (many projects like this are running on Kubernetes clusters).
  - A custom JSON encoder and decoder using [rapidjson](https://github.com/python-rapidjson/python-rapidjson).
  - Pytest testing with a basic conftest, flake8, coverage, and mypy.
  - Optional conda `environment.yaml` for creating a virtual environment with conda.


## Quick Start

-- Fill In...

Create a virtual environment and install depdendencies:




And open it in the browser at [http://localhost:8000/](http://localhost:8000/)

## Tests and Local Development

Make sure you have all testing requirements installed:

```sh
$ conda activate opinions
(opinions) $ pip install -r testing-requirements.txt
(opinions) $ pip install -e .
(opinions) $ pytest
```

## Deployment

```sh
$ docker build -t opinions .
$ docker run --rm -p 8000:8000 opinions:latest
```
