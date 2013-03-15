from flask import Flask
from flask.ext import Api, Rosurce
import os

app = Flask(__name__)
api = Api(app)

output = {
        "command": "ls -l",
        "output": ""
        }

class ListDirectory(Resource):
    def get(self):
        output["output"] = os.listdir("/home/victor/tmp")
        return output

api.add_resource(ListDirectory, "/")

if __name__ == '__main__':
    app.run(debug=True)

