# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import freeling
import json
import sys


# local setting
FREELINGDIR = "/usr/local/"
DATA = FREELINGDIR + "share/freeling/"
LANG = "es"
freeling.util_init_locale("default")

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
parser = freeling.chart_parser(DATA + LANG + "/chunker/grammar-chunk.dat")
#dep = freeling.dep_txala(DATA + LANG+ "/dep/dependences.dat", parser.get_start_symbol())


text = u"El perro de Juan se llama Bobby."
#text = u"Los gatos saltan y el perro come."
#text = u"El perro salta."


# tokenize and analyze the input string
tokens = tk.tokenize(text)
sentences = sp.split(tokens, 0)
sentences = mf.analyze(sentences)
sentences = tg.analyze(sentences)
sentences = sen.analyze(sentences)
sentences = parser.analyze(sentences)
#sentences = dep.analyze(sentences)

# <codecell>
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



for sentence in sentences:
    #print dict(parent="ROOT", value="S", id=0, children=True)
    tree = sentence.get_parse_tree()
    #output = [dict(tag="S", parent="ROOT", level=0)]
    output = []
    output = handleParsedTreeAsString(tree.begin(), 0, output)
    #print json.dumps(output)
    print json.dumps(dict(analysis=" ".join(output)))

