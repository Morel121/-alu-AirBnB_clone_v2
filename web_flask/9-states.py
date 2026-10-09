#!/usr/bin/python3
"""
Starts a Flask web application displaying States or a specific State by ID.
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Removes current SQLAlchemy Session after each request."""
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """Displays HTML page with all States or specific State by id."""
    all_states = storage.all(State)
    if id is not None:
        key = "State.{}".format(id)
        state = all_states.get(key)
        return render_template('9-states.html', state=state)
    states = sorted(list(all_states.values()), key=lambda x: x.name)
    return render_template('9-states.html', states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
