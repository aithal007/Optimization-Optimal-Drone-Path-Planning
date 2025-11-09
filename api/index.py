"""
Vercel serverless function wrapper for the Flask app
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from server import app

# Vercel expects a variable named 'app' or a handler function
# Flask app is already named 'app', so we just export it
handler = app
