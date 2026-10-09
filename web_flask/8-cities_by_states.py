#!/usr/bin/python3
"""
Starts a Flask web application listing States and their Cities.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Removes current SQLAlchemy Session after each request."""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Displays HTML page with States and their linked Cities."""
    states = sorted(list(storage.all(State).values()), key=lambda x: x.name)
    return render_template('8-cities_by_states.html', states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
