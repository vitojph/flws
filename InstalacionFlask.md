# Servicios web con flask y flask-restful

## Instalación de paquetes

[flask](http://flask.pocoo.org) es un pequeño servidor para Python que permite hacer aplicaciones (y servicios) web fácilmente, gracias a [flask-restful](http://flask-restful.readthedocs.org).


He tenido que instalar varias cosas:

1. `git` para el control de versiones. He montado un repo privado (por el
   momento) en [bitbucket](https://bitbucket.org).

    sudo aptitude install git

2. `pip` y `virtualenv` para instalar paquetes de Python en un entorno virtual
   seguro.

    sudo aptitude install python-pip
    sudo pip virtualenv

Me creo un entorno virtual y lo activo:

    cd flws
    virtualenv venv
    . venv/bin/activate

El resto de librerías de Python las instalo de manera virtual en virtualenv.

    pip install flask
    pip install flask-restful


