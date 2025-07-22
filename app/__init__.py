# app/__init__.py

from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Import routes after app initialization to avoid circular imports
from app import main