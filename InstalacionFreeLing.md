# Instalación de FreeLing Tools en servidor Ubuntu

Aunque existen paquetes con los binarios de FreeLing es recomendable instalando
compilando las fuentes. En las versiones actuales el proceso es sencillo y está
estandarizado con automake (es el típio `./configure && make && make install).

A continuación voy a describir los pasos que he seguido para compilar e instalar FreeLing en un servidor con Ubuntu. Usaré como referencia la sección [Installing from tar.gz sources packages](http://nlp.lsi.upc.edu/freeling/doc/userman/html/node12.html) del manual.


1. Descargo las fuentes de freeling desde la [página de descargas](http://devel.cpl.upc.edu/freeling/downloads?order=time&desc=1). La versión estable más moderna hoy (23/02/2013) es `freeling-3.0.tar.gz` del 22/10/2012.

    mkdir tmp
    cd tmp
    curl -o freeling-3.0.tar.gz http://devel.cpl.upc.edu/freeling/downloads/21


1. Para poder compilar las fuentes, instalo las herramientas de desarrollo: compilador de C++, `automake`
   y demás dependencias:

    sudo aptitude update
    sudo aptitude install build-essential automake autoconf

    Se instalarán los siguiente paquetes NUEVOS:     
    autoconf automake autotools-dev{a} binutils{a} build-essential cpp{a} cpp-4.6{a} dpkg-dev{a} fakeroot{a} 
    g++{a} g++-4.6{a} gcc{a} gcc-4.6{a} libalgorithm-diff-perl{a} libalgorithm-diff-xs-perl{a} 
    libalgorithm-merge-perl{a} libc-dev-bin{a} libc6-dev{a} libdpkg-perl{a} libgomp1{a} libmpc2{a} libmpfr4{a} 
    libquadmath0{a} libstdc++6-4.6-dev{a} linux-libc-dev{a} m4{a} make{a} manpages-dev{a} 
    0 paquetes actualizados, 28 nuevos instalados, 0 para eliminar y 5 sin actualizar.
    Necesito descargar 32,0 MB de archivos. Después de desempaquetar se usarán 88,0 MB.


   
1. Las versiones anteriores de FreeLing tenía muchas dependencias. La actual 3.0 solo tiene dos, que se pueden instalar fácilmente desde los repositorios oficiales de Ubuntu.

    Instalo los paquetes en dos tandas, tal y como dice el manual. Pero probablemente se pueda hacer todo de una vez. 


    sudo aptitude install libboost-regex-dev libicu-dev

    Se instalarán los siguiente paquetes NUEVOS:     
    libboost-regex-dev libboost-regex1.46-dev{a} libboost-regex1.46.1{a} libboost1.46-dev{a} libicu-dev libicu48{a} 
    0 paquetes actualizados, 6 nuevos instalados, 0 para eliminar y 5 sin actualizar.
    Necesito descargar 26,5 MB de archivos. Después de desempaquetar se usarán 115 MB.

    sudo aptitude install libboost-filesystem-dev libboost-program-options-dev

    Se instalarán los siguiente paquetes NUEVOS:     
    libboost-filesystem-dev libboost-filesystem1.46-dev{a} libboost-filesystem1.46.1{a} 
    libboost-program-options-dev libboost-program-options1.46-dev{a} libboost-program-options1.46.1{a} 
    libboost-system1.46-dev{a} libboost-system1.46.1{a} 
    0 paquetes actualizados, 8 nuevos instalados, 0 para eliminar y 5 sin actualizar.
    Necesito descargar 519 kB de archivos. Después de desempaquetar se usarán 2.454 kB.


1. Descomprimo las fuentes:

    tar xvzf FreeLing-3.0.tar.gz


1. Compruebo que tengo todas las herramientas necesarias y creo el `makefile`.
   El sistema imprime por pantalla todas las comprobaciones. Si hemos instalado
   todas las dependencias no debería saltar ningún warning.

    cd freeling-3.0/
    ./configure


1. Compilo. Es el paso más largo y el sistema escupe muchos mensajes:

    make


1. Instalo los binarios donde corresponde. En este caso necesito permisos de
   administrador.

    sudo make install


FreeLing es un conjunto de librerías de procesamiento diseñadas para ser invocadas desde otros programas. Las librerías se instalan por defecto en `/usr/local/lib/libfreeling.so`. Sin embargo, un ejecutable a modo de ejemlo instalado por defecto en `/usr/local/bin/analyzer`.

Blablabla
