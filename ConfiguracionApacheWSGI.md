# Deployment de Flask en Apache y configuración


Los servicios siguen funcionando en los mismos puertos pero solo responden desde 146.255.185.24, 87.218.2.105 y en local (127.0.0.1). 

En `/etc/apache2/sites-available/` he creado dos archivos de configuración para el servicio de identificación de idioma por el puerto 8880 (`langident`) y para los de análisis lingüístico del castellano en el puerto 8881 (`flwses`). 

En estos ficheros:

  1. utilizo WSGI (un interfaz para web services en Python) para arrancar los scripts, que están alojados en `/home/freelingr/public_html/freeling-api/`
  
  2. configuro los ficheros de logs, alojados en `/var/log/langident.log` y `/var/log/apache2/flws-es.log`.
  

En el fichero `/etc/apache2/ports.conf` he tenido que abrir los puertos necesarios.


