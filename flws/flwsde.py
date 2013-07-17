#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple flask-based API to access pattern.de functionalities.
"""

__author__ = "Víctor Peinado"
__email__ = "vitojph@gmail.com"
__date__ = "17/07/2013"


from pattern.de import parsetree
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
            output.append("+%s_[" % (node.get_label()))
        else:
            # if node has children but isn't head
            output.append("%s_[" % (node.get_label()))

        # for each children, repeat process
        for i in range(nch):
            child = tree.nth_child_ref(i)
            handleParsedTreeAsFL(child, depth+1, output)

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
            output.append(dict(text=w.get_form(), lemma=w.get_lemma(), tag=w.get_tag(), parent=parent.get_info().get_label(), level=depth))
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

        # set tagset: default is STTS
        try:
            tagset = request.json["tagset"]
        except KeyError:
            tagset = "stts"
        
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
            format = "json"

        # set tagset: default is STTS
        try:
            tagset = request.json["tagset"]
        except KeyError:
            tagset = "stts"
        
        # load the specified tagset
        if tagset == "penn":
            parsing = parsetree(text, relations=True, lemmata=True)
        else:
            parsing = parsetree(text, relations=True, lemmata=True, tagset=tagset)

        # TODO: vas por aquí
        if format == "string":
            parsedtree = handleParsedTreeAsString(parsing)
        elif format == "json":
            parsedtree = handleParsedTreeAsJSON(parsing)
        
        #  format the output accordingly
        if format == "string":
            return Response(json.dumps(dict(analisis=" ".join(parsedtree))), mimetype="application/json")
        elif format == "json":
            return Response(json.dumps(output), mimetype="application/json")




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
