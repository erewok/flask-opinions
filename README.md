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

Follow the instructions below to create an environment and run this project locally.

### Dependencies and Environment

Using conda, you can create a virtual environment and install depdendencies:

```sh
❯ conda env create -f environment.yaml
...
```

A `requirements.txt` file has also been provided for those who want to use another virtual environment tool (such as pyenv,
pipenv, etc).

Further, the `requirements.txt` dependency list is used for building a Docker image, because the equivalent Miniconda
images are large (2GB+) and somewhat unwieldy (activating and running projects takes more effort).

### Environment Variables and Secrets

This project demonstrates two different ways to retrieve secrets: from environment variables and from files.

To run the sample project, set the `OPINIONS_SECRETS_DIR` environment variable and make sure that a secret value is
present there under the filename `opinions-something-secret`:

```sh
❯ export OPINIONS_SECRETS_DIR=`pwd`

❯ echo "some-secret" > `pwd`/opinions-something-secret
```

You can also set the `OPINIONS_ENVIRONMENT` variable to trigger different behavior.

For instance, when the `environment` variable is set to `"local"`, the log output will have colors:

![Run.py Output Local](/docs/local_runpy_output.png)

However, when the `environment` variable is set to anything *other than* `"local"`, the log output will be JSON:

```sh
❯ export OPINIONS_ENVIRONMENT=dev

❯ python run.py
{"message": null, "environment": "dev", "event": "OPINIONS API started", "application": "opinions", "version": "0.0.1", "level": "info", "timestamp": "2019/10/06 01:51:19"}
{"message": " * Running on http://localhost:8000/ (Press CTRL+C to quit)", "timestamp": "2019-10-06T01:51:19.143931", "application": "opinions", "version": "0.0.1"}
{"message": " * Restarting with stat", "timestamp": "2019-10-06T01:51:19.144588", "application": "opinions", "version": "0.0.1"}
{"message": null, "environment": "dev", "event": "OPINIONS API started", "application": "opinions", "version": "0.0.1",
"level": "info", "timestamp": "2019/10/06 01:51:19"}
{"message": "127.0.0.1 - - [05/Oct/2019 18:52:11] \"GET /json HTTP/1.1\" 200 -", "timestamp": "2019-10-06T01:52:11.180039", "application": "opinions", "version": "0.0.1"}
```

Interestingly, you can use `jq` or other tools to parse these log outputs, but the reason for JSON is to facilitate
sending all logs _directly_ into a data store such as Elasticsearch.

Once you have the project running, you can open it in a browser at
[http://localhost:8000/](http://localhost:8000/)

### Profiling

We have found it helpful to include an option in our `run.py` script to trigger profiling in our projects:

```sh
❯ python run.py --profile
{"message": null, "environment": "dev", "event": "OPINIONS API started", "application": "opinions", "version": "0.0.1", "level": "info", "timestamp": "2019/10/06 04:07:55"}
{"message": " * Running on http://localhost:8000/ (Press CTRL+C to quit)", "timestamp": "2019-10-06T04:07:55.233406", "application": "opinions", "version": "0.0.1"}
{"message": " * Restarting with stat", "timestamp": "2019-10-06T04:07:55.234908", "application": "opinions", "version": "0.0.1"}
{"message": null, "environment": "dev", "event": "OPINIONS API started", "application": "opinions", "version": "0.0.1", "level": "info", "timestamp": "2019/10/06 04:07:55"}
{"message": "127.0.0.1 - - [05/Oct/2019 21:08:05] \"GET /json HTTP/1.1\" 200 -", "timestamp": "2019-10-06T04:08:05.542335", "application": "opinions", "version": "0.0.1"}
--------------------------------------------------------------------------------
PATH: '/json'
         301 function calls in 0.002 seconds

   Ordered by: internal time, call count
   List reduced from 128 to 30 due to restriction <30>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.002    0.002    0.002    0.002 /.../open_source/flask-opinions/opinions/json_encoding.py:25(jsonify)
        1    0.000    0.000    0.002    0.002 /.../miniconda3/envs/opinions/lib/python3.7/site-packages/werkzeug/middleware/profiler.py:96(runapp)
        9    0.000    0.000    0.000    0.000 /.../miniconda3/envs/opinions/lib/python3.7/site-packages/werkzeug/local.py:163(top)
        1    0.000    0.000    0.000    0.000 /.../miniconda3/envs/opinions/lib/python3.7/site-packages/werkzeug/routing.py:1466(bind_to_environ)
```


## Running Tests


You should also install the testing-requirements and the project itself, which makes path resolution in testing a bit simpler:

```sh
❯ conda activate opinions

(opinions) ❯ pip install -r testing-requirements.txt

(opinions) ❯ pip install -e .

(opinions) ❯ pytest

```

The tests are configured by `setup.cfg`, which instructs pytest to do the following:

- Collect and display code coverage in html form (see `htmlcov` directory after running the tests)
- Run flake8
- Run mypy (not implemented yet).


## Deployment

This project has a Dockerfile (based on Alpine) included for running it in production.

You can build and run the Docker container in the following way:

```sh
$ docker build -t opinions .
$ docker run --rm -e OPINIONS_SECRETS_DIR=/secrets -v `pwd`:/secrets -p 8000:8000 opinions:latest
{"message": null, "environment": "dev", "event": "OPINIONS API started", "application": "opinions", "version": "0.0.1", "level": "info", "timestamp": "2019/10/06 03:53:36"}
{"message": null, "environment": "dev", "event": "OPINIONS API started", "application": "opinions", "version": "0.0.1", "level": "info", "timestamp": "2019/10/06 03:53:36"}
{"message": null, "environment": "dev", "event": "OPINIONS API started", "application": "opinions", "version": "0.0.1", "level": "info", "timestamp": "2019/10/06 03:53:36"}
{"message": null, "function": "index", "endpoint": "/", "method": "GET", "version": "0.0.1", "event": "Get index", "application": "opinions", "level": "info", "timestamp": "2019/10/06 03:53:43"}
```

In addition, the project has a Kubernetes manifest (not implemented yet) for running it on a Kubernetes cluster.

### Continuous Integration

In order to simplify the requirements for our infrastructure team, we have standardized on using Docker containers to
run tests.

This makes our testing infrastructure _consistent_ with our deployment infrastructure (same environment variables are
required, for instance).

To build the testing dockerfile, run the following:

```sh
❯ docker build -f deployment/Dockerfile.test -t opinions:testing .
Sending build context to Docker daemon  8.136MB
Step 1/19 : FROM alpine:3.10.1
...
Successfully built 3cf99fdc05d3
Successfully tagged opinions:testing
```

Next, you can run it as follows:

```sh
❯ docker run --rm opinions:testing
============================= test session starts ==============================
platform linux -- Python 3.7.4, pytest-5.2.0, py-1.8.0, pluggy-0.13.0
rootdir: /app, inifile: setup.cfg
plugins: flask-0.15.0, flake8-1.0.4, cov-2.8.1, mypy-0.4.1
collected 26 items

Running mypy on 12 files... done with status 0
Success: no issues found in 12 source files

run.py ..                                                                [  7%]
setup.py ..                                                              [ 15%]
opinions/__init__.py ..                                                  [ 23%]
opinions/config.py ..                                                    [ 30%]
opinions/constants.py ..                                                 [ 38%]
opinions/core.py ..                                                      [ 46%]
opinions/json_encoding.py ..                                             [ 53%]
opinions/loggers.py ..                                                   [ 61%]
opinions/endpoints/__init__.py ..                                        [ 69%]
opinions/endpoints/base.py ..                                            [ 76%]
test/conftest.py ..                                                      [ 84%]
test/integration/test_endpoints/test_base.py ....                        [100%]

----------- coverage: platform linux, python 3.7.4-final-0 -----------
Coverage HTML written to dir htmlcov
Coverage XML written to file /app/htmlcov/coverage.xml


============================= 26 passed in 13.09s ==============================
```

### Azure DevOps Pipeline

-- To Do ---
