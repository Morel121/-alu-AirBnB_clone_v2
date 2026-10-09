#!/usr/bin/python3
"""
Starts a Flask web application rendering all states from DBStorage or FileStorage.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Removes current SQLAlchemy Session after each request."""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Displays HTML page with list of all State objects sorted by name."""
    states = sorted(list(storage.all(State).values()), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
