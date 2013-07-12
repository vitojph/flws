#!/usr/bin/env python
# -*- coding: utf-8 -*-


import freeling
import json

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
dep = freeling.dep_txala(DATA + LANG+ "/dep/dependences.dat", parser.get_start_symbol())


def handleParsedTree(output, node, depth):
    """Handles a parsed tree"""
    info = node.get_info()
    if info.is_head():
        output += "+"

    nch = node.num_children()
    if nch == 0:
        w = info.get_word()
        output += "%s %s %s" % (w.get_form(), w.get_lemma(), w.get_tag())
    else:
        output += "{ %s }_[" % (info.get_label())

        for i in range(nch):
            child = node.nth_child_ref(i)
            handleParsedTree(output, child, depth+1)

        output += "] "
        
    return output
    
    
def handleDepTree(tree, depth, output):
    """Handles a parsed tree"""
    node = tree.get_info()
    link = node.get_link()
    linfo = link.get_info()

    parentLabel = None
    if depth > 0:
        parentLabel = tree.get_parent().get_info().get_label()

    w = tree.get_info().get_word()
    output.append(dict(parent=parentLabel, rel=node.get_label(), label=link.get_info().get_label(), text=w.get_form(), lemma=w.get_lemma(), tag=w.get_tag()))

    nch = tree.num_children()
    if nch > 0:

        for i in range(nch):
            d = tree.nth_child_ref(i)
            if not d.get_info().is_chunk():
                handleDepTree(d, depth+1, output)

        ch = {}
        for i in range(nch):
            d = tree.nth_child_ref(i)
            if d.get_info().is_chunk():
                ch[d.get_info().get_chunk_ord()] = d
 
        for i in sorted(ch.keys()):
            handleDepTree(ch[i], depth+1, output)

    return output

 
#text = u"""Mi amigo Enrique partió hacia buen puerto el 4 de mayo. No he vuelto a saber de él. El equipo de los E.E.U.U. ha vencido a la URSS."""
text = u"El niño come manzanas. Mi perro se llama Bobby."

if __name__ == "__main__":
    # tokenize and analyze the input string
    tokens = tk.tokenize(text)
    sentences = sp.split(tokens, 0)
    sentences = mf.analyze(sentences)
    sentences = tg.analyze(sentences)
    sentences = sen.analyze(sentences)
    sentences = parser.analyze(sentences)
    sentences = dep.analyze(sentences)
    

#for sentence in sentences:
#    tree = sentence.get_parse_tree()
#    parsedtree = handleParsedTree("", tree.begin(), 0)    
#    print parsedtree
    
for sentence in sentences:
    tree = sentence.get_dep_tree()
    output = handleDepTree(tree.begin(), 0, [])
    print json.dumps(output)

