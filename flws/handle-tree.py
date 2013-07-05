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


#text = u"El perro de Juan se llama Bobby."
#text = u"Canto mal."
text = u"Pedro come manzanas."


# tokenize and analyze the input string
tokens = tk.tokenize(text)
sentences = sp.split(tokens, 0)
sentences = mf.analyze(sentences)
sentences = tg.analyze(sentences)
sentences = sen.analyze(sentences)
sentences = parser.analyze(sentences)
#sentences = dep.analyze(sentences)

# <codecell>

def handleParsedTree(l, tree, depth):
    """Handles a parsed tree: format proposed by Elena"""
    node = tree.get_info()
    nch = tree.num_children()
    
    # if node is head and has no children
    if nch == 0:
        if node.is_head():
                parent = tree.get_parent()
                w = node.get_word()
                #print dict(parent=parent.get_info().get_label(), value=w.get_tag(), id=depth, text=w.get_form(), children=False)
                l.append(dict(parent=parent.get_info().get_label(), value=w.get_tag(), id=depth, text=w.get_form(), children=False))
           
    else:
        parent = tree.get_parent()
        # for each children, repeat process
        for i in range(nch):
            if depth != 0:
                #print dict(parent=parent.get_info().get_label(), value=node.get_label(), id=depth, children=True)
                l.append(dict(parent=parent.get_info().get_label(), value=node.get_label(), id=depth, children=True))
            
            child = tree.nth_child_ref(i)
            handleParsedTree(l, child, depth+1)
    
    return l 




def buildFormat(l):
    """Transform de list of nodes into a nested structure. """
    # reordeno
    l.reverse()
    ll = l[:]
    i = 1

    for item in l:
        # convierto a lista los hijos, solo si no lo he hecho ya
        if not isinstance(item["children"], list):
            ll[l.index(item)]["children"] = []
        
        # cojo el elemento siguiente
        try:
            nextItem = l[ l.index(item)+1 ]
            #print "Evaluo", item["parent"], nextItem["value"]

            # convierto a lista los hijos del siguiente, solo si no lo he hecho ya
            if not isinstance(nextItem["children"], list):
                ll[ l.index(item)+1 ]["children"] = []
        
            if item["parent"] == nextItem["value"]:
                #print "+++"
                #print "+", item
                #print "+", nextItem
                ll[ l.index(item)+1 ]["children"].append(item)
                #ll.remove(item)
            else:
                pass
                #print "---"
                #print "-", item
                #print "-", nextItem

        except IndexError:
            previous = l[l.index(item)-1]
            ll[ l.index(item) ]["children"] = [previous]
            #ll.remove(previous)
            #print "!!!"
            #print "!", item
            #print "!", previous
        except Exception:
            raise
            #print sys.stderr.write(e)
            #sys.exit()

        #print "Iteracción", i
        #print ll[:i+1]
        #print 

        i += 1

    ll.reverse()
    print "*******************************************************"
    for item in ll:
        print item, "\n"
    
    print "+++++++++++++++++++++++++++++++++++++++"
    for item in list(ll):
        print item["parent"], "...", 
        if item["parent"] != "S":
            print "borrado"
            ll.remove(item)
        else:
            print
    
    return ll



# <codecell>

#tree = sentences[0].get_parse_tree()
#root = tree.begin()
#node = root.get_info()
#nch = root.num_children()
#child = root.nth_child_ref(3)
#print child.get_info().get_label()
#parent = child.get_parent()
#print parent.get_info().get_label()

# <codecell>

for sentence in sentences:
    #print dict(parent="ROOT", value="S", id=0, children=True)
    tree = sentence.get_parse_tree()    
    l = handleParsedTree([], tree.begin(), 0)
    #print l
    print buildFormat(l)

