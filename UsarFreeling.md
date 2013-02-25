# Cómo usar FreeLing

FreeLing es un conjunto de librerías en C++ pensadas para ser utilizadas desde
un programa nativo programado *ad hoc*. Aun así, cuando se instala, existe una
herramienta llamada `analyzer` (con *r*) que puede utilizarse para la mayoría de las
tareas de análisis y que da acceso a la mayor parte de las funcionalidades.

## FreeLing desde la línea de comandos: `analyzer`

Para utilizar `analyzer` se pueden especificar las opciones (lengua a analizar, formatos de
entrada y salida, tipo de análisis, etc.) por línea de comandos o en un fichero
de configuración. 

Los ficheros de configuración de ejemplo están en `/usr/local/share/freeling/config/`. Me hago una copia en mi directorio de usuario de los ficheros de configuración de español e inglés.

    cp /usr/local/share/freeling/config/e?.cfg .


Hay que asegurarse de que las variables de entorno que vienen definidas en los
archivos de configuración funcionan. Por si acaso:

    import FREELINGSHARE=/usr/local/share/freeling

Tengo un par de textos que quiero analizar: `ejemplo.txt` y `example.txt`. No
he tocado opciones de configuración y, por defecto, `analyzer` asume que le
paso texto sin etiquetar separado por oraciones (una oración por cada línea)
y que deberá devolver por la salida estándar lematización y análisis morfolófico.

Para ejecutar dicho el análisis en el ejemplo en español: 

    analyzer -f es.cfg < ejemplo.txt

Y para el inglés:

    analyzer -f en.cfg < example.txt



## FreeLing como servidor


Además, para probar, he lanzado un servidor Freeling con las opciones de lematizar y etiquetar morfológicamente textos en español con el siguiente comando (ojo, lanzo el ejecutable `analyze`, sin *r*).

    analyze -f es.cfg --server --port 8888

    SERVER: Analyzers loaded.

    Launched server 16084 at port 8888

    You can now analyze text with the following command:
        - From this computer: 
            analyzer_client 8888 <input.txt >output.txt
            analyzer_client localhost:8888 <input.txt >output.txt
        - From any other computer: 
            analyzer_client vps-molinodeideas05:8888 <input.txt >output.txt

    Stop the server with: 
          analyze stop 16084

    SERVER.DISPATCHER: Waiting for a free worker slot
    SERVER.DISPATCHER: Waiting connections


Para lanza un cliente que haga consultas desde el propio servidor, ejecuto:

    analyzer_client localhost:8888 < ejemplo.txt

    El el DA0MS0 1
    niño niño NCMS000 0.994505
    juega jugar VMIP3S0 0.822581
    con con SPS00 1
    la el DA0FS0 0.972269
    pelota pelota NCFS000 1
    mientras mientras CS 0.889785
    el el DA0MS0 1
    Sr._González sr._gonzález NP00000 1
    bebe beber VMIP3S0 0.994868
    vino vino NCMS000 0.569444
    . . Fp 1

    Argo argo NP00000 1
    se se P00CN000 0.465639
    impone imponer VMIP3S0 1
    ante ante SPS00 0.998084
    Lincoln lincoln NP00000 1
    en en SPS00 1
    una uno DI0FS0 0.951575
    dispersa disperso AQ0FS0 0.532154
    noche noche NCFS000 1
    de de SPS00 0.999984
    los el DA0MP0 0.976481
    Oscar oscar NP00000 1
    . . Fp 1

