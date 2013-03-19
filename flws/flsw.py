#!/usr/bin/env python

"""
Author: Víctor Peinado <vitojph@gmail.com>
Version: 0.1
Date: 15/03/2013
"""


from flask import Flask
from flask.ext import Api, Rosurce
import os

app = Flask(__name__)
api = Api(app)

output = {
        "command": "",
        "output": ""
        }

class Analyzer(Resource):
    def post(self, lang, informat, outformat):
        # select the server to be queried
        self.server = ""
        # build the command, from the options specified
        command = ""
        # execute the command
        # get the ouput from freeling analyzer
        # transform it, if needed
        # return the output

class ESAnalyzer(Analyzer):
    def __init__(self):
        self.server = "" # spanish analyzer
        self.locale = ""



class ENAnalyzer(Analyzer):
    defl __init__(self):
        self.server = "" # english analyzer
        self.locale = ""


api.add_resource(Analyzer, "/")



if __name__ == '__main__':
    app.run(debug=True)

