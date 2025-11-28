"""
Application entry point.
Run: flask run (or python run.py)
"""

import os
from app import create_app


if __name__ == '__main__':
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    app.run(debug=True, host='0.0.0.0', port=5000)
