import os
import server

env = os.environ.get('FLASK_ENV', 'development')
debug = env == 'development'
server.create_app({
    'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres@db:5432/'
})
server.load_db()
server.app.run(host='0.0.0.0', debug=debug)
