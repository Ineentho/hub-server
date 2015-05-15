import os
import server

env_flask_env = os.environ.get('FLASK_ENV') or 'development'
env_conn_string = os.environ.get('DATABASE_CONNECTION_STRING') or 'postgresql://postgres@db:5432/'


server.create_app({
    'SQLALCHEMY_DATABASE_URI': env_conn_string
})
server.load_db()
server.app.run(host='0.0.0.0', debug=(env_flask_env == 'development'))
