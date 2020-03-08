from flask import Flask

app = Flask(__name__)
from image.routes.Routes import *

app.config["DEBUG"] = True

if __name__ == "__main__":
    app.run()
