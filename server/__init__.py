from flask import Flask
app = Flask(__name__)

import server.auth
import server.public_api