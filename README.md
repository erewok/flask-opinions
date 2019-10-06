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


### Dependencies and Environment

Using conda, you can create a virtual environment and install depdendencies:

```sh
❯ conda env create -f environment.yaml
...
```

You should also install the testing-requirements and the project itself, which makes path resolution in testing a bit simpler:

```sh
❯ pip install -r testing-requirements.txt

❯ pip install -e .

```

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

```sh
❯ export OPINIONS_ENVIRONMENT=local

❯ python run.py
2019/10/06 01:34:11 [info     ] OPINIONS API started           application=opinions environment=local version=0.0.1
 * Running on http://localhost:8000/ (Press CTRL+C to quit)
 * Restarting with stat
2019/10/06 01:34:11 [info     ] OPINIONS API started           application=opinions environment=local version=0.0.1
2019/10/06 01:34:24 [info     ] Get index                      application=opinions endpoint=/ function=index method=GET version=0.0.1
```

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

Interestingly, you can use `jq` or other tools to parse these log outputs, but they're meant to go _directly_ into a
data store such as Elasticsearch.

Finally, once you have the project running, you can open it in a browser at
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


## Tests and Local Development

Make sure you have all testing requirements installed:

```sh
$ conda activate opinions
(opinions) $ pip install -r testing-requirements.txt
(opinions) $ pip install -e .
(opinions) $ pytest
```

## Deployment

This project has a Dockerfile (based on Alpine) included for running it in production.

You can build and run the Docker container in the following way:

```sh
$ docker build -t opinions .
$ docker run --rm -e OPINIONS_SECRETS_DIR=/secrets -v `pwd`:/secrets -p 8000:8000 opinions:latest
{"message": null, "environment": "dev", "event": "OPINIONS API started", "application": "opinions", "version": "0.0.1", "level": "info", "timestamp": "2019/10/06 03:53:36"}
{"message": null, "environment": "dev", "event": "OPINIONS API started", "application": "opinions", "version": "0.0.1", "level": "info", "timestamp": "2019/10/06 03:53:36"}
{"message": null, "environment": "dev", "event": "OPINIONS API started", "application": "opinions", "version": "0.0.1", "level": "info", "timestamp": "2019/10/06 03:53:36"}
{"message": null, "function": "index", "endpoint": "/", "method": "GET", "version": "0.0.1", "event": "Get index", "application": "opinions", "level": "info", "timestamp": "2019/10/06 03:53:43"} docker run --rm -p 8000:8000 opinions:latest
```
