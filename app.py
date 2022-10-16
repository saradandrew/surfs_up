# Import the Flask dependency
from flask import Flask

# Create a new Flask app instance
app = Flask(__name__)

# Define the root & add code
@app.route('/')
def hello_world():
    return 'Hello world'
