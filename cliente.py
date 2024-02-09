import socket as sk


cliente = sk.socket(sk.AF_INET, sk.SOCK_STREAM)


host = sk.gethostname()
port = 1234

cliente.connect((host, port))


if __name__ == "__main__":
    try:
        while True:
            msj = input("¿Qué mensaje quieres enviar? (escribe 'salir' para terminar): ")
            if msj.lower() == 'salir':  # Verificar si el usuario quiere salir
                break
            print(msj)
            cliente.send(msj.encode())
    finally:
        cliente.close()  # Asegurar que el socket se cierre correctamente


"""
 _________________________________________
/ Ya mejor no programes Hijo              /
 -----------------------------------------
   \
    \
        .--.
       |o_o |
       |:_/ |
      //   \ \
     (|     | )
    /'\_   _/`\
    \___)=(___/
"""