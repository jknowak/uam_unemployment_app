"""
Index of available apps as required by gunicorn
"""

from src.app import app

server = app.server

if __name__ == "__main__":
    app.run()
