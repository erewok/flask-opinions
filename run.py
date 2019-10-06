"""
run.py

Entrypoint for our Flask application object.

You can also use this module to run a version of this project locally
(assuming all required environment variables are availabled):

   $ python run.py
   python run.py
   {"message": null, "environment": "dev", "event": "Opinions API started"...
   {"message": " * Running on http://localhost:8000/ (Press CTRL+C to quit)"...
"""
from werkzeug.middleware.profiler import ProfilerMiddleware
from werkzeug.serving import run_simple

from opinions import core


app = core.create_app("opinions")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", action='store_true')
    parser.add_argument("--count-restriction")

    args = parser.parse_args()
    count = 30
    if args.count_restriction is not None:
        try:
            count = int(args.count_restriction)
        except TypeError:
            pass
    if args.profile:
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[count])

    # Run Flask app
    run_simple('localhost',
               8000,
               app,
               use_reloader=True)
