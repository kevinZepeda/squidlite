# ACL "Access Control List"

acl nombre_de_la_acl tipo_de_acl opciones

## Tipos de acl:

### src: Direcciones ip
acl red_local src 192.168.0.0/24  
acl ip_permitidas src "/etc/squid/ip-permitidas"
acl ip_bloqueadas src "/etc/squid/ip-bloqueadas"
acl rango_ip src 192.168.0.10-192.168.0.50/24

### dstdomain: dominios de páginas web
acl web_prohibidas dstdomain facebook.com
acl web_prohibidas dstdomain "/etc/squid/lista_web_prohibidas"
acl web_permitidas dstdomain .edu.co .org .gov.co
acl web_permitidas dstdomain "/etc/squid/lista_web_permitidas"

### url_regex: palabras en las url
acl palabras_prohibidas url_regex facebook
acl palabras_prohibidas url_regex "/etc/squid/palabras_prohibidas"


# Accesos HTTP
## Estructura Basica

http_access allow nombre_de_la_acl
```
En este caso se entregan permisos de navegación a las direcciones ip que esten dentro del rango de direcciones que tiene la acl de nombre red_local
```
http_access allow red_local  
```
Estos permisos se puede combinar en la misma linea junto con bloqueos, por ejemplo:
El signo de "!" indica que ese elemento esta prohibido a pesar de utilizarse un http_access allow
```
http_access allow red_local web_permitidas
http_access allow red_local !web_prohibidas !palabras_prohibidas
http_access deny rango_ip !lista_web_permitidas


# Respuesta HTTP
```
Es posible redirigir un a un dominio en caso de una denegacion de servicio 
```
deny_info http://sitio.para/redireccion
https_reply_access deny acl_bloaquado acl_grupo_usuario


# Redirector Program
url_rewrite_extras "%>a %>rm %un"
url_rewrite_children 3 startup=0 idle=1 concurrency=10
url_rewrite_program /usr/bin/python3.8 /etc/squid/redirect.py