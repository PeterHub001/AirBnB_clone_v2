#!/usr/bin/python3

from flask import Flask

# Create the Flask application
app = Flask(__name__)

# Import the routes module
from . import routes

