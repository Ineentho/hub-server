import os
from server import app

env = os.environ.get('FLASK_ENV', 'development')
debug = env == 'development'
app.run(host='0.0.0.0', debug=debug)