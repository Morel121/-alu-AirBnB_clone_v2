#!/usr/bin/python3
"""
Starts a Flask web application displaying HBNB dynamic filters page.
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Removes current SQLAlchemy Session after each request."""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Renders dynamic 10-hbnb_filters.html page with States, Cities, and Amenities."""
    states = sorted(list(storage.all(State).values()), key=lambda x: x.name)
    amenities = sorted(list(storage.all(Amenity).values()), key=lambda x: x.name)
    return render_template('10-hbnb_filters.html', states=states, amenities=amenities)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
