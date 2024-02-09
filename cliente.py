import socket as sk


def main():
    cliente = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

    host = sk.gethostname()
    port = 1234

    try:
        cliente.connect((host, port))
        while True:
            msj = input(
                "¿Qué mensaje quieres enviar? (escribe 'salir' para terminar): ")
            if msj.lower() == 'salir':
                break
            print(msj)
            cliente.send(msj.encode())
    finally:
        print("Socket del cliente cerrado")
        cliente.close()


if __name__ == "__main__":
    main()


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
