import socket
nombre_equipo = socket.gethostname()
direccion_equipo = socket.gethostbyname(nombre_equipo)
print(direccion_equipo)