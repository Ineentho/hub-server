import os
from flask import Flask

print('asd')
app = Flask(__name__)


@app.route("/")
def hello():
    return "aHello World!faaaa"

print(__name__ + 'name')

if __name__ == "__main__":
    env = os.environ.get('FLASK_ENV', 'development')
    debug = False
    if env == 'development':
        debug = True
    app.run(host='0.0.0.0', debug=debug)