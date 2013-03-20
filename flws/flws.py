#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple flask-based API to access FreeLing functionalities.
"""

__author__ = "Víctor Peinado"
__email__ = "vitojph@gmail.com"
__date__ = "20/03/2013"


import freeling
from flask import Flask
from flask.ext.restful import Api, Resource, reqparse


# #################################################################
# FreeLing settings (borrowed from freeling-3.0/APIs/python/sample.py)

## Modify this line to be your FreeLing installation directory
FREELINGDIR = "/usr/local/"
DATA = FREELINGDIR + "share/freeling/"
LANG = "es"
freeling.util_init_locale("default");

# Create language analyzer
#la=freeling.lang_ident(DATA + "common/lang_ident/ident.dat")

# Create options set for maco analyzer. Default values are Ok, except for data files.
op = freeling.maco_options(LANG)
op.set_active_modules(0,1,1,1,1,1,1,1,1,1,0)
op.set_data_files("",
        DATA + LANG + "/locucions.dat", 
        DATA + LANG + "/quantities.dat", 
        DATA + LANG + "/afixos.dat", 
        DATA + LANG + "/probabilitats.dat", 
        DATA + LANG + "/dicc.src", 
        DATA + LANG + "/np.dat",
        DATA + "common/punct.dat",
        DATA + LANG + "/corrector/corrector.dat")

# Create analyzers
tk = freeling.tokenizer(DATA + LANG + "/tokenizer.dat")
sp = freeling.splitter(DATA + LANG + "/splitter.dat")
mf = freeling.maco(op)
tg = freeling.hmm_tagger(LANG, DATA + LANG + "/tagger.dat", 1, 2)
sen = freeling.senses(DATA+LANG+"/senses.dat")
#parser = freeling.chart_parser(DATA + LANG + "/chunker/grammar-chunk.dat")
#dep = freeling.dep_txala(DATA + LANG+ "/dep/dependences.dat", parser.get_start_symbol())


# #################################################################
# flask API

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("text", type=unicode)



# Create output
#output = dict(command="", output="")


class Analyzer(Resource):
    """FreeLing Analyzer"""

    def post(self):
        """docstring for post"""
        args = parser.parse_args()
        text = unicode(args["text"])
        # tokenize and analyze the input string
        tokens = tk.tokenize(text)
        sentences = sp.split(tokens, 0)
        #if inpf == "":
        sentences = mf.analyze(sentences)
        sentences = tg.analyze(sentences)
        sentences = sen.analyze(sentences)
        #ls = parser.analyze(ls)
        #ls = dep.analyze(ls)
       
        output = []
        for sentence in sentences:
            words = sentence.get_words()
            for word in words:
                output.append([word.get_form(), word.get_lemma(), word.get_tag(), word.get_senses_string()])
                #output.append(word.get_form())
        return output

    ## output results
#    for s in ls :
#       ws = s.get_words();
#       for w in ws :
#          print(w.get_form()+" "+w.get_lemma()+" "+w.get_tag()+" "+w.get_senses_string());
#       print ("");

#       tr = s.get_parse_tree();
#       printTree(tr.begin(), 0);

#       dp = s.get_dep_tree();
#       printDepTree(dp.begin(), 0)


class ShowText(Resource):
    """docstring for ShowText"""
    def get(self):
        return "Hola amigo"


api.add_resource(Analyzer, "/analyzer")
api.add_resource(ShowText, "/")

if __name__ == '__main__':
    app.run(debug=True)

