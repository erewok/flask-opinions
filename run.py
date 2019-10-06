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

from werkzeug.serving import run_simple

from opinion import core


app = core.create_app("opinions")

if __name__ == "__main__":
    # Run Flask app
    run_simple('localhost',
               8000,
               app,
               use_reloader=True)
