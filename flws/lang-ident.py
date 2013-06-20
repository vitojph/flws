#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple flask-based API to access FreeLing's language identifier.
"""

__author__ = "Víctor Peinado"
__email__ = "vitojph@gmail.com"
__date__ = "20/06/2013"


import freeling
from flask import Flask, Response, request
from flask.ext.restful import Api, Resource
import json

# #################################################################
# FreeLing settings (borrowed from freeling-3.0/APIs/python/sample.py)

## Modify this line to be your FreeLing installation directory
FREELINGDIR = "/usr/local/"
DATA = FREELINGDIR + "share/freeling/"
LANG = "es"
freeling.util_init_locale("default");

# Create language analyzer
la=freeling.lang_ident(DATA + "common/lang_ident/ident.dat")


# #################################################################
# flask API

app = Flask(__name__)
api = Api(app)


# ##############################################################################

class LanguageIdentifier(Resource):
    """Identifies the language of the input text."""
    
    def post(self):
        text = request.json["texto"]
        output=[]
        output.append(dict(lang=la.identify_language(text, [])))

        return Response(json.dumps(output), mimetype="application/json")



# #############################################################################
# Api resource routing

# split a text into sentences
api.add_resource(LanguageIdentifier, "/lang")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8880)
    #app.run(host="0.0.0.0")
