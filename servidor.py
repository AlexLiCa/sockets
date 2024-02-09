import socket as sk


def main():

    server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

    ip = "127.0.0.1"
    port = 1234

    host = sk.gethostname()
    print(f"Host: {host}")
    try:
        server.bind((host, port))
    except sk.error as e:
        print(f"Error al bincular el socket: {e}")
        return False

    server.listen(1)
    print("Server esperando")
    try:
        while True:
            conn, addr = server.accept()
            with conn:
                print(f"Connection from {addr}")
                while True:
                    msj = conn.recv(1024).decode()
                    if not msj or msj.lower() == 'salir':
                        break
                    print(f"Mensaje: {msj}")
                    print("-"*30)
                    
    except sk.error as e:
        print(f"Error de conexion: {e}")

    finally:
        print("Cerrando el servidor")
        server.close()


if __name__ == "__main__":
    main()
