# Servicios disponibles

Ahora mismo tengo dos servicios diferentes, cada uno por un puerto diferente:

1. **identificación de idioma** (puerto `8881`). El proceso de cargas de frecuencias es bastante pesado, por eso lo arranco por separado.

2. **análisis lingüístico del español** (puerto `8881`).

3. **análisis lingüístico del catalán** (puerto `8882`).

4. **análisis lingüístico del inglés** (puerto `8883`).




## Identificación de idioma

    curl http://146.255.185.75:8880/lang -H "Content-Type:application/json" -d '{"texto":"Mira que coisa mais linda."}' -X POST -s
    [{"lang": "pt"}]

    curl http://146.255.185.75:8880/lang -H "Content-Type:application/json" -d '{"texto":"Sono appena arrivato da Milan."}' -X POST -s 
    [{"lang": "it"}]


## Segmentador de oraciones

    curl http://146.255.185.75:8881/splitter -H "Content-Type:application/json" -d '{"texto":"El presidente del Atleti hace pelis. Me gusta el jamón. Mucho."}' -X POST -s
    [{"oracion": "El presidente del Atleti hace pelis ."}, {"oracion": "Me gusta el jam\u00f3n ."}, {"oracion": "Mucho ."}]


## Segmentador de oraciones y tokenizador

    curl http://146.255.185.75:8881/tokenizersplitter -H "Content-Type:application/json" -d '{"texto":"El presidente del Atleti hace pelis. Me gusta el jamón. Mucho."}' -X POST -s
    [{"oracion": ["El", "presidente", "del", "Atleti", "hace", "pelis", "."]}, {"oracion": ["Me", "gusta", "el", "jam\u00f3n", "."]}, {"oracion": ["Mucho", "."]}]


## Etiquetador morfológico

    curl http://146.255.185.75:8881/tagger -H "Content-Type:application/json" -d '{"texto":"El presidente del Atleti hace pelis. Me gusta el jamón. Mucho."}' -X POST -s
    [{"palabra": "El", "lemas": [{"categoria": "DA0MS0", "lema": "el"}]}, {"palabra": "presidente", "lemas": [{"categoria": "NCMS000", "lema": "presidente"}]}, {"palabra": "de", "lemas": [{"categoria": "SPS00", "lema": "de"}]}, {"palabra": "el", "lemas": [{"categoria": "DA0MS0", "lema": "el"}]}, {"palabra": "Atleti", "lemas": [{"categoria": "NP00000", "lema": "atleti"}]}, {"palabra": "hace", "lemas": [{"categoria": "VMIP3S0", "lema": "hacer"}]}, {"palabra": "pelis", "lemas": [{"categoria": "RG", "lema": "pelis"}]}, {"palabra": ".", "lemas": [{"categoria": "Fp", "lema": "."}]}, {"palabra": "Me", "lemas": [{"categoria": "PP1CS000", "lema": "me"}]}, {"palabra": "gusta", "lemas": [{"categoria": "VMIP3S0", "lema": "gustar"}]}, {"palabra": "el", "lemas": [{"categoria": "DA0MS0", "lema": "el"}]}, {"palabra": "jam\u00f3n", "lemas": [{"categoria": "NCMS000", "lema": "jam\u00f3n"}]}, {"palabra": ".", "lemas": [{"categoria": "Fp", "lema": "."}]}, {"palabra": "Mucho", "lemas": [{"categoria": "RG", "lema": "mucho"}]}, {"palabra": ".", "lemas": [{"categoria": "Fp", "lema": "."}]}]


## Etiquetadir morfológico y desambiguador semántico

    curl http://146.255.185.75:8881/wsdtagger -H "Content-Type:application/json" -d '{"texto":"El presidente del Atleti hace pelis. Me gusta el jamón. Mucho."}' -X POST -s
    [{"synsets": [""], "palabra": "El", "lemas": [{"categoria": "DA0MS0", "lema": "el"}]}, {"synsets": ["10467179-n", "10467395-n", "10468559-n", "10468962-n", "10469346-n"], "palabra": "presidente", "lemas": [{"categoria": "NCMS000", "lema": "presidente"}]}, {"synsets": [""], "palabra": "de", "lemas": [{"categoria": "SPS00", "lema": "de"}]}, {"synsets": [""], "palabra": "el", "lemas": [{"categoria": "DA0MS0", "lema": "el"}]}, {"synsets": [""], "palabra": "Atleti", "lemas": [{"categoria": "NP00000", "lema": "atleti"}]}, {"synsets": ["00107369-v", "00120675-v", "00184786-v", "00730758-v", "00770437-v", "01617192-v", "01619014-v", "01621555-v", "01641545-v", "01645601-v", "01646075-v", "01653873-v", "01663920-v", "01712704-v", "01733477-v", "01753788-v", "01754737-v", "02355596-v", "02367363-v", "02560585-v", "02560767-v", "02561995-v", "02562901-v", "02582921-v", "02598483-v", "02621133-v"], "palabra": "hace", "lemas": [{"categoria": "VMIP3S0", "lema": "hacer"}]}, {"synsets": [""], "palabra": "pelis", "lemas": [{"categoria": "RG", "lema": "pelis"}]}, {"synsets": [""], "palabra": ".", "lemas": [{"categoria": "Fp", "lema": "."}]}, {"synsets": [""], "palabra": "Me", "lemas": [{"categoria": "PP1CS000", "lema": "me"}]}, {"synsets": ["01776952-v", "01777210-v", "01820302-v", "01824736-v"], "palabra": "gusta", "lemas": [{"categoria": "VMIP3S0", "lema": "gustar"}]}, {"synsets": [""], "palabra": "el", "lemas": [{"categoria": "DA0MS0", "lema": "el"}]}, {"synsets": ["07669891-n"], "palabra": "jam\u00f3n", "lemas": [{"categoria": "NCMS000", "lema": "jam\u00f3n"}]}, {"synsets": [""], "palabra": ".", "lemas": [{"categoria": "Fp", "lema": "."}]}, {"synsets": ["00059086-r", "00059171-r", "00092047-r"], "palabra": "Mucho", "lemas": [{"categoria": "RG", "lema": "mucho"}]}, {"synsets": [""], "palabra": ".", "lemas": [{"categoria": "Fp", "lema": "."}]}]


## Reconocedor de entidades nombradas

    curl http://146.255.185.75:8881/ner -H "Content-Type:application/json" -d '{"texto":"La ONU dice que I.B.M. no tiene sede en Francia sino E.E.U.U."}' -X POST -s 
    [{"entidades": [{"categoria": "NP00000", "lema": "onu"}], "palabra": "ONU"}, {"entidades": [{"categoria": "NP00000", "lema": "i.b.m."}], "palabra": "I.B.M."}, {"entidades": [{"categoria": "NP00000", "lema": "francia"}], "palabra": "Francia"}]


## Reconocedor de fechas, cantidades y monedas

    curl http://146.255.185.75:8881/datesquantities -H "Content-Type:application/json" -d '{"texto":"Llego el martes a las siete menos cuarto. Los diez kilos de tomates me costaron 35 euros. Llegó a 30 km/h."}' -X POST -s
    [{"expresion": "martes_a_las_siete_menos_cuarto", "entidades": [{"categoria": "temporal", "lema": "[M:??/??/??:6.45:??]"}]}, {"expresion": "diez", "entidades": [{"categoria": "numero", "lema": "10"}]}, {"expresion": "35_euros", "entidades": [{"categoria": "moneda", "lema": "$_ECU:35"}]}, {"expresion": "30_km_/_h", "entidades": [{"categoria": "magnitud", "lema": "SP_km/h:30"}]}]


## Analizador sintáctico

    curl http://127.0.0.1:8881/parser -H "Content-Type:application/json" -d '{"texto":"María es la hermana de mi vecino Antonio y vive en Madrid."}' -X POST -s
    {"analisis": "S_[ sn_[ +grup-nom-ms_[ +w-ms_[ +(Mar\u00eda mar\u00eda NP00000) ] ] ] grup-verb_[ +verb_[ +(es ser VSIP3S0) ] ] sn_[ espec-fs_[ +j-fs_[ +(la el DA0FS0) ] ] +grup-nom-fs_[ +n-fs_[ +(hermana hermano NCFS000) ] ] ] sp-de_[ +(de de SPS00) sn_[ espec-ms_[ +pos-ms_[ +(mi mi DP1CSS) ] ] +grup-nom-ms_[ +n-ms_[ +(vecino vecino NCMS000) ] w-ms_[ +(Antonio antonio NP00000) ] ] ] ] coord_[ +(y y CC) ] grup-verb_[ +verb_[ +(vive vivir VMIP3S0) ] ] grup-sp_[ +prep_[ +(en en SPS00) ] sn_[ +grup-nom-ms_[ +w-ms_[ +(Madrid madrid NP00000) ] ] ] ] F-term_[ +(. . Fp) ] ]"}


