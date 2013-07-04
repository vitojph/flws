# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

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
#dep = freeling.dep_txala(DATA + LANG+ "/dep/dependences.dat", parser.get_start_symbol())

text = u"El perro de Juan se llama Bobby."

# tokenize and analyze the input string
tokens = tk.tokenize(text)
sentences = sp.split(tokens, 0)
sentences = mf.analyze(sentences)
sentences = tg.analyze(sentences)
sentences = sen.analyze(sentences)
sentences = parser.analyze(sentences)
#sentences = dep.analyze(sentences)

# <codecell>

def handleParsedTree(tree, depth):
    """Handles a parsed tree: format proposed by Elena"""
    node = tree.get_info()
    nch = tree.num_children()
    
    # if node is head and has no children
    if node.is_head() and nch == 0:
            parent = tree.get_parent()
            w = node.get_word()
            print dict(parent=parent.get_label(), value=w.get_tag(), id=depth, text=w.get_form(), children=False)
           
    else:
        parent = tree.get_parent()
        # for each children, repeat process
        for i in range(nch):

            print dict(parent=parent.get_label(), value=node.get_label(), id=depth, children=True)
            child = tree.nth_child_ref(i)
            print handleParsedTree(child, depth+1)

    return

# <codecell>

tree = sentences[0].get_parse_tree()
root = tree.begin()
node = root.get_info()
nch = root.num_children()
child = root.nth_child_ref(3)
print child.get_info().get_label()
parent = child.get_parent()
print parent.get_info().get_label()

# <codecell>

for sentence in sentences:
    tree = sentence.get_parse_tree()    
    handleParsedTree(tree.begin(), 0)

# <codecell>

def recorre(output, tree, depth):
    """Handles a parsed tree"""
    node = tree.get_info()
    nch = tree.num_children()
    s = {}
    
    
    
    # if node is head and has no children
    if nch == 0:
        if node.is_head():
            w = info.get_word()
            output.append("%s/%s/%s" % (w.get_form(), w.get_lemma(), w.get_tag()))
    else:
        # if node is head and has children
        if node.is_head():
            output.append("(%s " % (info.get_label()))
        else:
            # if node has children but isn't head
            output.append("%s( " % (info.get_label()))

        # for each children, repeat process
        for i in range(nch):
            child = node.nth_child_ref(i)
            handleParsedTree(output, child, depth+1)

        # close node
        output.append(") ")

    return output

