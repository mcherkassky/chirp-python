#!flask/bin/python
from chirp import app

# If this is the main module, run this code.
if __name__ == "__main__":
    app.run(use_reloader=False, port=5000)