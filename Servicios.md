# Servicios REST de FreeLing

Todos los servicios utilizan el API de [FreeLing](http://nlp.lsi.upc.edu/freeling/), excepto las herramientas de análisis para alemán y neerlandés, que se apoyan en [`pattern`](http://www.clips.ua.ac.be/pages/pattern).

Ahora mismo están funcionando nueve servicios, cada uno por un puerto diferente:

1. **identificación de idioma** (puerto `8880`). El proceso de cargas de frecuencias es bastante pesado, por eso lo arranco por separado.

2. **análisis lingüístico del español** (puerto `8881`).

3. **análisis lingüístico del catalán** (puerto `8882`).

4. **análisis lingüístico del inglés** (puerto `8883`).

5. **análisis lingüístico del bable** (puerto `8884`).

6. **análisis lingüístico del gallego** (puerto `8885`).

7. **análisis lingüístico del italiano** (puerto `8886`).

8. **análisis lingüístico del portugués** (puerto `8887`).

9. **análisis lingüístico del ruso** (puerto `8888`).

10. **análisis lingüístico del alemán** (puerto `8889`).

11. **análisis lingüístico del neerlandés** (puerto `8890`).


## Servicios diponibles por lengua

                                            ES CA EN AS GL IT PT RU DE NL
    Segmentador de oraciones                X  X  X  X  X  X  X  X  X  X
    Segmentador de oraciones y tokenizador  X  X  X  X  X  X  X  X  X  X
    Etiquetador morfológico                 X  X  X  X  X  X  X  X  X  X
    Etiquetador morfológico y desambiguador X  X  X     X  X  X
    Reconocedor de entidades                X  X  X  X  X  X  X
    Reconocedor de fechas y cantidades      X  X  X  X  X  X  X  X
    Analizador sintáctico                   X  X  X  X  X     X     X  X 
    Analizador de dependencias              X  X  X     X


# Ejemplos

## Identificación de idioma `http://127.0.0.1:8880/lang`

Argumentos de entrada: 

- `texto`: *texto de entrada* 

Salida:

- *lista de elementos* `lang`:`es|ca|en|fr|gl|it|pt|ru|de|none`


        curl http://127.0.0.1:8880/lang -H "Content-Type:application/json" -d '{"texto":"Mira que coisa mais linda."}' -X POST -s
        [{"lang": "pt"}]

        curl http://127.0.0.1:8880/lang -H "Content-Type:application/json" -d '{"texto":"Sono appena arrivato da Milano."}' -X POST -s 
        [{"lang": "it"}]


## Segmentador de oraciones `splitter`

Argumentos: 

- `texto`:*texto de entrada*

Salida:

- *lista de elementos* `oracion`: *texto de la oración*


    curl http://127.0.0.1:8881/splitter -H "Content-Type:application/json" -d '{"texto":"La ONU dice que I.B.M. no tiene sede en Francia sino en EEUU. Te espero el lunes a las tres menos cuarto."}' -X POST -s
    [{"oracion": "La ONU dice que I.B.M. no tiene sede en Francia sino en EEUU ."}, {"oracion": "Te espero el lunes a las tres menos cuarto ."}]


## Segmentador de oraciones y tokenizador `tokenizersplitter`

Argumentos: 

- `texto`: *texto de entrada*

Salida:

- *lista de elementos* `oracion`: *lista de tokens*


    curl http://127.0.0.1:8889/tokenizersplitter -H "Content-Type:application/json" -d '{"texto":"Die SIM-Karte ist eine kleine Chip-Karte, die im Handy platziert wird. Sie enthält Informationen über das verwendete Mobilfunknetz und Zusatzdienste wie SMS und MMS. Zum Verwenden der SIM-Karte muss zunächst eine PIN am Handy eingegeben werden."}' -X POST -s
    [{"oracion": ["Die", "SIM-Karte", "ist", "eine", "kleine", "Chip-Karte", ",", "die", "im", "Handy", "platziert", "wird", "."]}, {"oracion": ["Sie", "enth\u00e4lt", "Informationen", "\u00fcber", "das", "verwendete", "Mobilfunknetz", "und", "Zusatzdienste", "wie", "SMS", "und", "MMS", "."]}, {"oracion": ["Zum", "Verwenden", "der", "SIM-Karte", "muss", "zun\u00e4chst", "eine", "PIN", "am", "Handy", "eingegeben", "werden", "."]}]


## Etiquetador morfológico `tagger`

Argumentos: 

- `texto`: *texto de entrada*
- para los servicios basados en pattern, hay un argumento opcional llamado `tagset`: `stts` (alemán)`|woten` (neerlandés)`|penn`

Salida:

- *lista de hashes* `palabra`: *palabra*, `lemas`: *lista de hashes* `categoria`:
  *etiqueta gramatical*, `lema`: *lema*


    curl http://127.0.0.1:8881/tagger -H "Content-Type:application/json" -d '{"texto":"El presidente del Atleti hace pelis. Me gusta el jamón. Mucho."}' -X POST -s
    [{"palabra": "El", "lemas": [{"categoria": "DA0MS0", "lema": "el"}]}, {"palabra": "presidente", "lemas": [{"categoria": "NCMS000", "lema": "presidente"}]}, {"palabra": "de", "lemas": [{"categoria": "SPS00", "lema": "de"}]}, {"palabra": "el", "lemas": [{"categoria": "DA0MS0", "lema": "el"}]}, {"palabra": "Atleti", "lemas": [{"categoria": "NP00000", "lema": "atleti"}]}, {"palabra": "hace", "lemas": [{"categoria": "VMIP3S0", "lema": "hacer"}]}, {"palabra": "pelis", "lemas": [{"categoria": "RG", "lema": "pelis"}]}, {"palabra": ".", "lemas": [{"categoria": "Fp", "lema": "."}]}, {"palabra": "Me", "lemas": [{"categoria": "PP1CS000", "lema": "me"}]}, {"palabra": "gusta", "lemas": [{"categoria": "VMIP3S0", "lema": "gustar"}]}, {"palabra": "el", "lemas": [{"categoria": "DA0MS0", "lema": "el"}]}, {"palabra": "jam\u00f3n", "lemas": [{"categoria": "NCMS000", "lema": "jam\u00f3n"}]}, {"palabra": ".", "lemas": [{"categoria": "Fp", "lema": "."}]}, {"palabra": "Mucho", "lemas": [{"categoria": "RG", "lema": "mucho"}]}, {"palabra": ".", "lemas": [{"categoria": "Fp", "lema": "."}]}]

    curl http://127.0.0.1:8889/tagger -H "Content-Type:application/json" -d '{"texto":"Die SIM-Karte ist eine kleine Chip-Karte, die im Handy platziert wird.", "tagset":"stts"}' -X POST -s
    [{"palabra": "Die", "lemas": [{"categoria": "ARTDEF", "lema": "die"}]}, {"palabra": "SIM-Karte", "lemas": [{"categoria": "NN", "lema": "sim-karte"}]}, {"palabra": "ist", "lemas": [{"categoria": "VVFIN", "lema": "ist"}]}, {"palabra": "eine", "lemas": [{"categoria": "ARTIND", "lema": "eine"}]}, {"palabra": "kleine", "lemas": [{"categoria": "ADJA", "lema": "kleine"}]}, {"palabra": "Chip-Karte", "lemas": [{"categoria": "NN", "lema": "chip-karte"}]}, {"palabra": ",", "lemas": [{"categoria": "C", "lema": ","}]}, {"palabra": "die", "lemas": [{"categoria": "PRELS", "lema": "die"}]}, {"palabra": "im", "lemas": [{"categoria": "APPRART", "lema": "im"}]}, {"palabra": "Handy", "lemas": [{"categoria": "NE", "lema": "handy"}]}, {"palabra": "platziert", "lemas": [{"categoria": "NE", "lema": "platziert"}]}, {"palabra": "wird", "lemas": [{"categoria": "VAFIN", "lema": "wird"}]}, {"palabra": ".", "lemas": [{"categoria": "S", "lema": "."}]}]

    curl http://127.0.0.1:8890/tagger -H "Content-Type:application/json" -d '{"texto":"Rodríguez is Mollema en Ten Dam voorbij in het algemeen klassement en staat inmiddels vijfde.", "tagset": "woten"}' -X POST -s

    curl http://127.0.0.1:8890/tagger -H "Content-Type:application/json" -d '{"texto":"Rodríguez is Mollema en Ten Dam voorbij lgemeen klassement en staat inmiddels vijfde.", "tagset": "woten"}' -X POST -s
[{"palabra": "Rodr\u00edguez", "lemas": [{"categoria": "N(eigen,ev)", "lema": "rodr\u00edguez"}]}, {"palabra": "is", "lemas": [{"categoria": "V(hulp_of_kopp,ott,3,ev)", "lema": "is"}]}, {"palabra": "Mollema", "lemas": [{"categoria": "N(eigen,ev)", "lema": "mollema"}]}, {"palabra": "en", "lemas": [{"categoria": "Conj(neven)", "lema": "en"}]}, {"palabra": "Ten", "lemas": [{"categoria": "Prep(voor)", "lema": "ten"}]}, {"palabra": "Dam", "lemas": [{"categoria": "N(eigen,ev)", "lema": "dam"}]}, {"palabra": "voorbij", "lemas": [{"categoria": "Adv(deel_v)", "lema": "voorbij"}]}, {"palabra": "in", "lemas": [{"categoria": "Prep(voor)", "lema": "in"}]}, {"palabra": "het", "lemas": [{"categoria": "Art(bep,onzijd,neut)", "lema": "het"}]}, {"palabra": "algemeen", "lemas": [{"categoria": "N(soort,ev,neut)", "lema": "algemeen"}]}, {"palabra": "klassement", "lemas": [{"categoria": "N(soort,ev,neut)", "lema": "klassement"}]}, {"palabra": "en", "lemas": [{"categoria": "Conj(neven)", "lema": "en"}]}, {"palabra": "staat", "lemas": [{"categoria": "V(intrans,ott,3,ev)", "lema": "staat"}]}, {"palabra": "inmiddels", "lemas": [{"categoria": "Adv(gew,geen_func,stell,onverv)", "lema": "inmiddels"}]}, {"palabra": "vijfde", "lemas": [{"categoria": "Num(rang,bep,attr,onverv)", "lema": "vijfde"}]}, {"palabra": ".", "lemas": [{"categoria": "Punc(punt)", "lema": "."}]}]


## Etiquetadir morfológico y desambiguador semántico `wsdtagger`

Argumentos: 

- `texto`: *texto de entrada*

Salida:

- *lista de hashes* `synsts`: *IDs de los synsets*, `palabra`: *palabra*, `lemas`: *lista de hashes* `categoria`:
  *etiqueta gramatical*, `lema`: *lema*


    curl http://127.0.0.1:8881/wsdtagger -H "Content-Type:application/json" -d '{"texto":"El presidente del Atleti hace pelis. Me gusta el jamón. Mucho."}' -X POST -s
    [{"synsets": [""], "palabra": "El", "lemas": [{"categoria": "DA0MS0", "lema": "el"}]}, {"synsets": ["10467179-n", "10467395-n", "10468559-n", "10468962-n", "10469346-n"], "palabra": "presidente", "lemas": [{"categoria": "NCMS000", "lema": "presidente"}]}, {"synsets": [""], "palabra": "de", "lemas": [{"categoria": "SPS00", "lema": "de"}]}, {"synsets": [""], "palabra": "el", "lemas": [{"categoria": "DA0MS0", "lema": "el"}]}, {"synsets": [""], "palabra": "Atleti", "lemas": [{"categoria": "NP00000", "lema": "atleti"}]}, {"synsets": ["00107369-v", "00120675-v", "00184786-v", "00730758-v", "00770437-v", "01617192-v", "01619014-v", "01621555-v", "01641545-v", "01645601-v", "01646075-v", "01653873-v", "01663920-v", "01712704-v", "01733477-v", "01753788-v", "01754737-v", "02355596-v", "02367363-v", "02560585-v", "02560767-v", "02561995-v", "02562901-v", "02582921-v", "02598483-v", "02621133-v"], "palabra": "hace", "lemas": [{"categoria": "VMIP3S0", "lema": "hacer"}]}, {"synsets": [""], "palabra": "pelis", "lemas": [{"categoria": "RG", "lema": "pelis"}]}, {"synsets": [""], "palabra": ".", "lemas": [{"categoria": "Fp", "lema": "."}]}, {"synsets": [""], "palabra": "Me", "lemas": [{"categoria": "PP1CS000", "lema": "me"}]}, {"synsets": ["01776952-v", "01777210-v", "01820302-v", "01824736-v"], "palabra": "gusta", "lemas": [{"categoria": "VMIP3S0", "lema": "gustar"}]}, {"synsets": [""], "palabra": "el", "lemas": [{"categoria": "DA0MS0", "lema": "el"}]}, {"synsets": ["07669891-n"], "palabra": "jam\u00f3n", "lemas": [{"categoria": "NCMS000", "lema": "jam\u00f3n"}]}, {"synsets": [""], "palabra": ".", "lemas": [{"categoria": "Fp", "lema": "."}]}, {"synsets": ["00059086-r", "00059171-r", "00092047-r"], "palabra": "Mucho", "lemas": [{"categoria": "RG", "lema": "mucho"}]}, {"synsets": [""], "palabra": ".", "lemas": [{"categoria": "Fp", "lema": "."}]}]


## Reconocedor de entidades nombradas `ner`

Argumentos: 

- `texto`: *texto de entrada*

Salida:

- *lista de hashes* `palabra`: *palabra*, `entidades`: *lista de hashes* `categoria`:
  *etiqueta gramatical*, `lema`: *lema*


    curl http://127.0.0.1:8881/ner -H "Content-Type:application/json" -d '{"texto":"La ONU dice que I.B.M. no tiene sede en Francia sino en EEUU."}' -X POST -s
    [{"entidades": [{"categoria": "NP00000", "lema": "onu"}], "palabra": "ONU"}, {"entidades": [{"categoria": "NP00000", "lema": "i.b.m."}], "palabra": "I.B.M."}, {"entidades": [{"categoria": "NP00000", "lema": "francia"}], "palabra": "Francia"}, {"entidades": [{"categoria": "NP00000", "lema": "eeuu"}], "palabra": "EEUU"}]


## Reconocedor de fechas, cantidades y monedas `datesquantities`

Argumentos: 

- `texto`: *texto de entrada*

Salida:

- *lista de hashes* `expresión`: *expresión temporal/numérica*, `entidades`:
  *lista de hashes* `categoria: temporal|numero|partitivo|moneda|porcentaje|magnitud|numero`, `lema`: *expresión temporal/numércia formalizada*


    curl http://127.0.0.1:8881/datesquantities -H "Content-Type:application/json" -d '{"texto":"Llego el martes a las siete menos cuarto. Los diez kilos de tomates me costaron 35 euros. Llegó a 30 km/h."}' -X POST -s
    [{"expresion": "martes_a_las_siete_menos_cuarto", "entidades": [{"categoria": "temporal", "lema": "[M:??/??/??:6.45:??]"}]}, {"expresion": "diez", "entidades": [{"categoria": "numero", "lema": "10"}]}, {"expresion": "35_euros", "entidades": [{"categoria": "moneda", "lema": "$_ECU:35"}]}, {"expresion": "30_km_/_h", "entidades": [{"categoria": "magnitud", "lema": "SP_km/h:30"}]}]


## Analizador sintáctico `parser`

Argumentos: 

- `texto`: *texto de entrada*
- `format`: `json|string` (servicios basados en `pattern`) o `json|string|fl`
  (servicios basados en `FreeLing`)
- para los servicios basados en pattern, hay un argumento opcional llamado `tagset`: `stts` (alemán)`|woten` (neerlandés)`|penn`

Salida:

- Para la salida basada jerárquica basada en FreeLing (`fl`) o con paréntesis (`string`):
  
  - *hash* `tree`: *cadena con formato jerárquico*


    curl http://127.0.0.1:8890/parser -H "Content-Type:application/json" -d '{"texto":"Rodríguez is Mollema en Ten Dam voorbij in het algemeen klassement en staat inmiddels vijfde.", "tagset": "penn", "format": "string"}' -X POST -s
    {"tree": "S( NP( Rodr\u00edguez/rodr\u00edguez/NNP ) VP( is/zijn/MD ) NP( Mollema/mollema/NNP ) CC( en/en/CC ) PNP( PP( Ten/ten/IN NP( Dam/dam/NNP ) ) ) RP( voorbij/voorbij/RP ) PNP( PP( in/in/IN NP( het/het/DT algemeen/algemeen/NN klassement/klassement/NN ) ) ) CC( en/en/CC ) VP( staat/staan/VBZ ) ADVP( inmiddels/inmiddels/RB ) CD( vijfde/vijfde/CD ) .( ././. ) )"}


    curl http://127.0.0.1:8881/parser -H "Content-Type:application/json" -d '{"texto":"María es la hermana de mi vecino Antonio y vive en Madrid.", "format":"fl"}' -X POST -s
    {"tree": "S_[ sn_[ +grup-nom-ms_[ +w-ms_[ +(Mar\u00eda mar\u00eda NP00000) ] ] ] grup-verb_[ +verb_[ +(es ser VSIP3S0) ] ] sn_[ espec-fs_[ +j-fs_[ +(la el DA0FS0) ] ] +grup-nom-fs_[ +n-fs_[ +(hermana hermano NCFS000) ] ] ] sp-de_[ +(de de SPS00) sn_[ espec-ms_[ +pos-ms_[ +(mi mi DP1CSS) ] ] +grup-nom-ms_[ +n-ms_[ +(vecino vecino NCMS000) ] w-ms_[ +(Antonio antonio NP00000) ] ] ] ] coord_[ +(y y CC) ] grup-verb_[ +verb_[ +(vive vivir VMIP3S0) ] ] grup-sp_[ +prep_[ +(en en SPS00) ] sn_[ +grup-nom-ms_[ +w-ms_[ +(Madrid madrid NP00000) ] ] ] ] F-term_[ +(. . Fp) ] ]"}


- Para la salida en JSON:

    - *lista de hashes* `tag`: *etiqueta*, `parent`: *etiqueta del nodo superior*, `level`: *nivel en la jerarquía*.

    - Cuando el nodo es una hoja sin hijos, el formato de salida es:
        - *lista de hashes* `tag`: *etiqueta*, `parent`: *etiqueta del nodo superior*, `level`: *nivel en la jerarquía* 


    curl http://127.0.0.1:8881/parser -H "Content-Type:application/json" -d '{"texto":"María es la hermana de mi vecino Antonio y vive en Madrid.", "format":"json"}' -X POST -s
    [{"tag": "S", "parent": "ROOT", "level": 0}, {"tag": "sn", "parent": "S", "level": 1}, {"tag": "grup-nom-ms", "parent": "sn", "level": 2}, {"tag": "w-ms", "parent": "grup-nom-ms", "level": 3}, {"lemma": "mar\u00eda", "level": 4, "tag": "NP00000", "parent": "w-ms", "text": "Mar\u00eda"}, {"tag": "grup-verb", "parent": "S", "level": 1}, {"tag": "verb", "parent": "grup-verb", "level": 2}, {"lemma": "ser", "level": 3, "tag": "VSIP3S0", "parent": "verb", "text": "es"}, {"tag": "sn", "parent": "S", "level": 1}, {"tag": "espec-fs", "parent": "sn", "level": 2}, {"tag": "j-fs", "parent": "espec-fs", "level": 3}, {"lemma": "el", "level": 4, "tag": "DA0FS0", "parent": "j-fs", "text": "la"}, {"tag": "grup-nom-fs", "parent": "sn", "level": 2}, {"tag": "n-fs", "parent": "grup-nom-fs", "level": 3}, {"lemma": "hermano", "level": 4, "tag": "NCFS000", "parent": "n-fs", "text": "hermana"}, {"tag": "sp-de", "parent": "S", "level": 1}, {"lemma": "de", "level": 2, "tag": "SPS00", "parent": "sp-de", "text": "de"}, {"tag": "sn", "parent": "sp-de", "level": 2}, {"tag": "espec-ms", "parent": "sn", "level": 3}, {"tag": "pos-ms", "parent": "espec-ms", "level": 4}, {"lemma": "mi", "level": 5, "tag": "DP1CSS", "parent": "pos-ms", "text": "mi"}, {"tag": "grup-nom-ms", "parent": "sn", "level": 3}, {"tag": "n-ms", "parent": "grup-nom-ms", "level": 4}, {"lemma": "vecino", "level": 5, "tag": "NCMS000", "parent": "n-ms", "text": "vecino"}, {"tag": "w-ms", "parent": "grup-nom-ms", "level": 4}, {"lemma": "antonio", "level": 5, "tag": "NP00000", "parent": "w-ms", "text": "Antonio"}, {"tag": "coord", "parent": "S", "level": 1}, {"lemma": "y", "level": 2, "tag": "CC", "parent": "coord", "text": "y"}, {"tag": "grup-verb", "parent": "S", "level": 1}, {"tag": "verb", "parent": "grup-verb", "level": 2}, {"lemma": "vivir", "level": 3, "tag": "VMIP3S0", "parent": "verb", "text": "vive"}, {"tag": "grup-sp", "parent": "S", "level": 1}, {"tag": "prep", "parent": "grup-sp", "level": 2}, {"lemma": "en", "level": 3, "tag": "SPS00", "parent": "prep", "text": "en"}, {"tag": "sn", "parent": "grup-sp", "level": 2}, {"tag": "grup-nom-ms", "parent": "sn", "level": 3}, {"tag": "w-ms", "parent": "grup-nom-ms", "level": 4}, {"lemma": "madrid", "level": 5, "tag": "NP00000", "parent": "w-ms", "text": "Madrid"}, {"tag": "F-term", "parent": "S", "level": 1}, {"lemma": ".", "level": 2, "tag": "Fp", "parent": "F-term", "text": "."}]


## Analizador de dependencias `dep`

Argumentos: 

- `texto`:*texto de entrada*

Salida:

- *lista de hashes* `parent`: *etiqueta del nodo superior*, `rel`: *tipo de dependencia*, `label`: *etiqueta del nodo*, `text`: *palabra*, `lemma`: *lema*, `tag`: *etiqueta morfológica de la palabra*.


    curl http://127.0.0.1:8883/dep -H "Content-Type:application/json" -d '{"texto":"Many low-wage workers who won judgments were never paid."}' -X POST -s
    [{"lemma": "be", "tag": "VBD", "rel": "top", "parent": null, "text": "were", "label": "claus"}, {"lemma": "worker", "tag": "NNS", "rel": "ncsubj", "parent": "top", "text": "workers", "label": "sn-chunk"}, {"lemma": "many", "tag": "PRP", "rel": "modnomatch", "parent": "ncsubj", "text": "Many", "label": "PRP"}, {"lemma": "low-wage", "tag": "JJ", "rel": "ncmod", "parent": "ncsubj", "text": "low-wage", "label": "attrib"}, {"lemma": "who", "tag": "WP", "rel": "cmod", "parent": "ncsubj", "text": "who", "label": "rel-cl"}, {"lemma": "win", "tag": "VBD", "rel": "ccomp", "parent": "cmod", "text": "won", "label": "rel"}, {"lemma": "judgment", "tag": "NNS", "rel": "dobj", "parent": "ccomp", "text": "judgments", "label": "n-chunk"}, {"lemma": "never", "tag": "RB", "rel": "ncmod", "parent": "top", "text": "never", "label": "adv"}, {"lemma": "pay", "tag": "VBN", "rel": "cmod", "parent": "top", "text": "paid", "label": "vb-chunk"}, {"lemma": ".", "tag": "Fp", "rel": "ta", "parent": "top", "text": ".", "label": "st-brk"}]


    curl http://127.0.0.1:8881/dep -H "Content-Type:application/json" -d '{"texto":"María es la hermana de mi vecino Antonio y vive en Madrid.", "format":"fl"}' -X POST -s
    [{"lemma": "y", "tag": "CC", "rel": "top", "parent": null, "text": "y", "label": "coor-vb"}, {"lemma": "ser", "tag": "VSIP3S0", "rel": "co-v", "parent": "top", "text": "es", "label": "grup-verb"}, {"lemma": "mar\u00eda", "tag": "NP00000", "rel": "subj", "parent": "co-v", "text": "Mar\u00eda", "label": "sn"}, {"lemma": "hermano", "tag": "NCFS000", "rel": "att", "parent": "co-v", "text": "hermana", "label": "sn"}, {"lemma": "el", "tag": "DA0FS0", "rel": "espec", "parent": "att", "text": "la", "label": "espec-fs"}, {"lemma": "de", "tag": "SPS00", "rel": "sp-mod", "parent": "att", "text": "de", "label": "sp-de"}, {"lemma": "vecino", "tag": "NCMS000", "rel": "obj-prep", "parent": "sp-mod", "text": "vecino", "label": "sn"}, {"lemma": "mi", "tag": "DP1CSS", "rel": "espec", "parent": "obj-prep", "text": "mi", "label": "espec-ms"}, {"lemma": "antonio", "tag": "NP00000", "rel": "sn-mod", "parent": "obj-prep", "text": "Antonio", "label": "w-ms"}, {"lemma": "vivir", "tag": "VMIP3S0", "rel": "co-v", "parent": "top", "text": "vive", "label": "grup-verb"}, {"lemma": "en", "tag": "SPS00", "rel": "sp-obj", "parent": "co-v", "text": "en", "label": "grup-sp"}, {"lemma": "madrid", "tag": "NP00000", "rel": "obj-prep", "parent": "sp-obj", "text": "Madrid", "label": "sn"}, {"lemma": ".", "tag": "Fp", "rel": "modnomatch", "parent": "top", "text": ".", "label": "F-term"}]
