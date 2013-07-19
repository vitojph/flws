#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple flask-based API to access pattern.nl functionalities.
"""

__author__ = "Víctor Peinado"
__email__ = "vitojph@gmail.com"
__date__ = "19/07/2013"


from pattern.nl import parsetree, Word
from flask import Flask, Response, request
from flask.ext.restful import Api, Resource
import json

# #################################################################
# FreeLing settings (borrowed from freeling-3.0/APIs/python/sample.py)

PUNCTUATION = u""".,;:!? """


# #################################################################
# flask API

app = Flask(__name__)
api = Api(app)


# ##############################################################################
def handleParsedTreeAsString(parsedTree):
    """Handles a pattern parsed tree and transforms it into a S(entence)"""
    output = []

    for sentence in parsedTree:
        output.append("S(")
        for chunk in sentence.constituents(pnp=True):
            output.append("%s(" % chunk.type)
            # handle PNP chunks
            if isinstance(chunk, Word):
                output.append("%s/%s/%s" % (chunk.string, chunk.lemma, chunk.tag))
            else:
                if chunk.type == "PNP":
                    for ch in chunk.chunks:
                        output.append("%s(" % ch.type)
                        for word in ch.words:
                            output.append("%s/%s/%s" % (word.string, word.lemma, word.tag))
                    output.append(")")
                    output.append(")")
                else:
                    for word in chunk.words:
                        output.append("%s/%s/%s" % (word.string, word.lemma, word.tag))
                        
                
            output.append(")")
        output.append(")")
    
    return output
    
    
    
# ##############################################################################

def handleParsedTreeAsJSON(parsedTree):
    """Handles a pattern parsed tree and transforms it into a structured JSON format"""
    output = []
    parent = "ROOT"
    depth = 0

    for sentence in parsedTree:
        output.append(dict(tag="S", parent=parent, level=depth))
        for chunk in sentence.constituents(pnp=True):
            depth = 1
            parent = "S"
            output.append(dict(tag=chunk.type, parent=parent, level=depth))
            # handle PNP chunks
            if isinstance(chunk, Word):
                output.append(dict(text=chunk.string, lemma=chunk.lemma, tag=chunk.tag, parent=chunk.type, level=depth+1))
            else:
                parent = chunk.type
                depth = 2
                if chunk.type == "PNP":
                    for ch in chunk.chunks:
                        output.append(dict(tag=ch.type, parent=parent, level=depth))
                        parent = ch.type
                        depth = 3
                        for word in ch.words:
                            output.append(dict(text=word.string, lemma=word.lemma, tag=word.tag, parent=parent, level=depth))
                else:
                    for word in chunk.words:
                        output.append(dict(text=word.string, lemma=word.lemma, tag=word.tag, parent=parent, level=depth))
    
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


class Tagger(Resource):
    """Performs POS tagging from an input text."""

    def post(self):
        """docstring for post"""
        text = request.json["texto"]
 
        # set output format: default is json
        try:
            format = request.json["format"]
        except KeyError:
            format = "json"

        # set tagset: default is WOTAN
        try:
            tagset = request.json["tagset"]
        except KeyError:
            tagset = "wotan"
        
        # load the specified tagset
        if tagset == "penn":
            parsedTree = parsetree(text, relations=True, lemmata=True)
        else:
            parsedTree = parsetree(text, relations=True, lemmata=True, tagset=tagset)

        output = []
        for sentence in parsedTree:
            for word in sentence:
                lemmas = []
                lemmas.append(dict(lema=word.lemma, categoria=word.pos))
                output.append(dict(palabra=word.string, lemas=lemmas))
        
        return Response(json.dumps(output), mimetype="application/json")



# ##############################################################################

class Parser(Resource):
    """FreeLing parser with three output formats: freeling-like, stanford-like and jsonified"""

    def post(self):
        """docstring for post"""
        text = request.json["texto"]
 
        # set output format: default is json
        try:
            format = request.json["format"]
        except KeyError:
            format = "string"

        # set tagset: default is WOTAN
        try:
            tagset = request.json["tagset"]
        except KeyError:
            tagset = "wotan"
        
        # load the specified tagset
        if tagset == "penn":
            parsing = parsetree(text, relations=True, lemmata=True)
        else:
            parsing = parsetree(text, relations=True, lemmata=True, tagset=tagset)

        if format == "string":
            parsedtree = handleParsedTreeAsString(parsing)
        elif format == "json":
            parsedtree = handleParsedTreeAsJSON(parsing)
        
        #  format the output accordingly
        if format == "string":
            return Response(json.dumps(dict(tree=" ".join(parsedtree))), mimetype="application/json")
        elif format == "json":
            return Response(json.dumps(parsedtree), mimetype="application/json")




# #############################################################################
# Api resource routing
# split a text into sentences
#api.add_resource(Splitter, "/splitter")

# split a text into tokenized sentences
#api.add_resource(TokenizerSplitter, "/tokenizersplitter")

# perform PoS tagging from an input text
api.add_resource(Tagger, "/tagger")

# returns a parsed tree
api.add_resource(Parser, "/parser")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=9999)
