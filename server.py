##
#WEB server
##
#import webserver2
import socketserver
#import practica5
import practica6
#import pruebas12
PORT = 8008




#Handler = http.server.SimpleHTTPRequestHandler - te muestra los ficheros que hay en el directorio
Handler = practica6.testHTTPRequestHandler

#handler es una clase: le pasa la peticion al cliente
httpd = socketserver.TCPServer(("", PORT), Handler)
#la d de httpd es de demon del lenguaje unix.
print("serving at port", PORT)
httpd.serve_forever()
