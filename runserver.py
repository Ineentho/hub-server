import os
import server

env = os.environ.get('FLASK_ENV', 'development')
debug = env == 'development'
server.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/lib/data/db.sqlite'
server.load()
server.app.run(host='0.0.0.0', debug=debug)
