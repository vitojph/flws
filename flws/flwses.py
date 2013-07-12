#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple flask-based API to access FreeLing functionalities.
"""

__author__ = "Víctor Peinado"
__email__ = "vitojph@gmail.com"
__date__ = "26/06/2013"


import freeling
from flask import Flask, Response, request
from flask.ext.restful import Api, Resource
import json

# #################################################################
# FreeLing settings (borrowed from freeling-3.0/APIs/python/sample.py)

PUNCTUATION = u""".,;:!? """

## Modify this line to be your FreeLing installation directory
FREELINGDIR = "/usr/local/"
DATA = FREELINGDIR + "share/freeling/"
LANG = "es"
freeling.util_init_locale("default");

# Create options set for maco analyzer. Default values are Ok, except for data files.
op = freeling.maco_options(LANG)
op.set_active_modules(0,1,1,1,1,1,1,1,1,1,1)
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
parser = freeling.chart_parser(DATA + LANG + "/chunker/grammar-chunk.dat")
#dep = freeling.dep_txala(DATA + LANG+ "/dep/dependences.dat", parser.get_start_symbol())


# #################################################################
# flask API

app = Flask(__name__)
api = Api(app)


# ##############################################################################
def handleParsedTreeAsFL(tree, depth, output):
    """Handles a parsed tree"""
    node = tree.get_info()
    nch = tree.num_children()

    # if node is head and has no children
    if nch == 0:
        if node.is_head():
            w = node.get_word()
            output.append("+(%s %s %s)" % (w.get_form(), w.get_lemma(), w.get_tag()))
    else:
        # if node is head and has children
        if node.is_head():
            output.append("+%s_[" % (info.get_label()))
        else:
            # if node has children but isn't head
            output.append("%s_[" % (info.get_label()))

        # for each children, repeat process
        for i in range(nch):
            child = tree.nth_child_ref(i)
            handleParsedTree(child, depth+1, output)

        # close node
        output.append("]")

    return output


# ##############################################################################
def handleParsedTreeAsString(tree, depth, output):
    """Handles a parsed tree"""
    node = tree.get_info()
    nch = tree.num_children()
    parent = tree.get_parent()

    # if node is head and has no children
    if nch == 0:
        if node.is_head():
            w = node.get_word()
            output.append(u"%s/%s/%s" % (w.get_form(), w.get_lemma(), w.get_tag()))
    else:
        if depth > 0:
            output.append(u"%s(" % node.get_label())
        # for each children, repeat process
        for i in range(nch):
            child = tree.nth_child_ref(i)
            handleParsedTreeAsString(child, depth+1, output)
        
        if depth > 0:
            output.append(u")")

    return output


# ##############################################################################
def handleParsedTreeAsJSON(tree, depth, output):
    """Handles a parsed tree"""
    node = tree.get_info()
    nch = tree.num_children()
    parent = tree.get_parent()

    # if node is head and has no children
    if nch == 0:
        if node.is_head():
            w = node.get_word()
            output.append(dict(text=w.get_form(), tag=w.get_tag(), parent=parent.get_info().get_label(), level=depth))
    else:
        if depth > 0:
            output.append(dict(tag=node.get_label(), parent=parent.get_info().get_label(), level=depth))
        # for each children, repeat process
        for i in range(nch):
            child = tree.nth_child_ref(i)
            handleParsedTreeAsJSON(child, depth+1, output)

    return output


# ##############################################################################

class Splitter(Resource):
    """Splits an input text into sentences."""
    
    def post(self):
        text = request.json["texto"]
        if text[-1] not in PUNCTUATION: 
            text = text + "."
        tokens = tk.tokenize(text)
        sentences = sp.split(tokens, 0)
        
        # output list of sentences
        outputSentences = []
 
        for sentence in sentences:
            outputTokens = []
            for w in sentence.get_words():
                outputTokens.append(w.get_form())
            outputSentences.append(dict(oracion=" ".join(outputTokens)))
    
        return Response(json.dumps(outputSentences), mimetype="application/json")



class TokenizerSplitter(Resource):
    """Splits an input text into tokenized sentences."""
    
    def post(self):
        text = request.json["texto"]
        if text[-1] not in PUNCTUATION: 
            text = text + "."
        tokens = tk.tokenize(text)
        sentences = sp.split(tokens, 0)
        
        # output list of sentences
        outputSentences = []
        
        for sentence in sentences:
            outputTokens = []
            for w in sentence.get_words():
                outputTokens.append(w.get_form())
            outputSentences.append(dict(oracion=outputTokens))
    
        return Response(json.dumps(outputSentences), mimetype="application/json")


# ##############################################################################

class NERecognizer(Resource):
    """Recognizes Named Entities from an input text."""
    
    def post(self):
        text = request.json["texto"]
        if text[-1] not in PUNCTUATION: 
            text = text + "."
        tokens = tk.tokenize(text)
        sentences = sp.split(tokens, 0)
        sentences = mf.analyze(sentences)
        sentences = tg.analyze(sentences)
        
        output = []
        for sentence in sentences:
            words = sentence.get_words()
            for word in words:
                # Person (NP00SP0), Geographical location (NP00G00), Organization (NP00O00), and Others (NP00V00)
                if word.get_tag() in "NP00SP0 NP00G00 NP00000 NP00V00".split():
                    entities = []
                    entities.append(dict(lema=word.get_lemma(), categoria=word.get_tag()))
                    output.append(dict(palabra=word.get_form(), entidades=entities))

        sentences, words = [], []
        return Response(json.dumps(output), mimetype="application/json")


# ##############################################################################

class DatesQuatitiesRecognizer(Resource):
    """Recognizes dates, currencies, and quatities from an input text."""
    
    def post(self):
        #args = parser.parse_args()
        text = request.json["texto"]
        if text[-1] not in PUNCTUATION: 
            text = text + "."
        tokens = tk.tokenize(text)
        sentences = sp.split(tokens, 0)
        sentences = mf.analyze(sentences)
        sentences = tg.analyze(sentences)
        
        output = []
        for sentence in sentences:
            words = sentence.get_words()
            for word in words:
                # dates
                tag = word.get_tag()
                if tag[0] in "W Z".split():
                    expression = []
                    if tag == "W":
                        expression.append(dict(lema=word.get_lemma(), categoria="temporal"))
                    else:
                        if tag == "Z":
                            category = "numero"
                        elif tag == "Zd":
                            category = "partitivo"
                        elif tag == "Zm":
                            category = "moneda"
                        elif tag == "Zp":
                            category = "porcentaje"
                        elif tag == "Zu":
                            category = "magnitud"
                        else:
                            category = "numero"
                                                        
                        expression.append(dict(lema=word.get_lemma(), categoria=category))
                                        
                    output.append(dict(expresion=word.get_form(), entidades=expression))

        return Response(json.dumps(output), mimetype="application/json")



# ##############################################################################


class Tagger(Resource):
    """Performs POS tagging from an input text."""

    def post(self):
        """docstring for post"""
        text = request.json["texto"]
        if text[-1] not in PUNCTUATION: 
            text = text + "."
        tokens = tk.tokenize(text)
        sentences = sp.split(tokens, 0)
        sentences = mf.analyze(sentences)
        sentences = tg.analyze(sentences)

        output = []
        for sentence in sentences:
            words = sentence.get_words()
            for word in words:
                lemmas = []
                lemmas.append(dict(lema=word.get_lemma(), categoria=word.get_tag()))
                output.append(dict(palabra=word.get_form(), lemas=lemmas))
        
        return Response(json.dumps(output), mimetype="application/json")


# ##############################################################################


class WSDTagger(Resource):
    """Performs POS tagging and WSD from an input text."""

    def post(self):
        """docstring for post"""
        text = request.json["texto"]
        if text[-1] not in PUNCTUATION: 
            text = text + "."
        tokens = tk.tokenize(text)
        sentences = sp.split(tokens, 0)
        sentences = mf.analyze(sentences)
        sentences = tg.analyze(sentences)
        sentences = sen.analyze(sentences)

        output = []
        for sentence in sentences:
            words = sentence.get_words()
            for word in words:
                lemmas = []
                lemmas.append(dict(lema=word.get_lemma(), categoria=word.get_tag()))
                # split the senses and get just the synset ID
                synsets = []
                [synsets.append(synsetID.split(":")[0]) for synsetID in word.get_senses_string().split("/")]
                output.append(dict(palabra=word.get_form(), lemas=lemmas, synsets=synsets))

        return Response(json.dumps(output), mimetype="application/json")


# ##############################################################################


class Parser(Resource):
    """FreeLing parser: output in three formats: freeling, stanford and jsonified"""

    def post(self, format):
        """docstring for post"""
        text = request.json["texto"]
        format = request.json["format"]

        if text[-1] not in PUNCTUATION: 
            text = text + "."
        tokens = tk.tokenize(text)
        sentences = sp.split(tokens, 0)
        sentences = mf.analyze(sentences)
        sentences = tg.analyze(sentences)
        sentences = sen.analyze(sentences)
        sentences = parser.analyze(sentences)

        for sentence in sentences:
            tree = sentence.get_parse_tree()
            if format == "fl":
                parsedtree = handleParsedTreeAsFL(tree.begin(), 0, [])
            elif format == "string":
                parsedtree = handleParsedTreeAsString(tree.begin(), 0, [])
            elif format == "json":
                parsedtree = [dict(tag="S", parent="ROOT", level=0)]
                parsedtree = handleParsedTreeAsJSON(tree.begin(), 0, parsedtree)
                        
        return Response(json.dumps(dict(analisis=" ".join(parsedtree))), mimetype="application/json")


# ###############################################################################
class DependencyParser(Resource):
    """FreeLing Dependency Parser"""

    def post(self):
        pass




# #############################################################################
# Api resource routing
# split a text into sentences
api.add_resource(Splitter, "/splitter")

# split a text into tokenized sentences
api.add_resource(TokenizerSplitter, "/tokenizersplitter")

# perform PoS tagging from an input text
api.add_resource(Tagger, "/tagger")

# perform PoS tagging and WSD from an input text
api.add_resource(WSDTagger, "/wsdtagger")

# perform NE recognition from an input text
api.add_resource(NERecognizer, "/ner")

# recognizes dates, currencies and quantities
api.add_resource(DatesQuatitiesRecognizer, "/datesquantities")

# returns a parsed tree
api.add_resource(Parser, "/parser")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=9999)
