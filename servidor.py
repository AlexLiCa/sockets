import socket as sk

server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

ip = "127.0.0.1"
port = 1234

host = sk.gethostname()
print(f"Host: {host}")

server.bind((host, port))

server.listen(1)

if __name__ == "__main__":
    print("Server esperando")
    try:
        while True:
            conn, addr = server.accept()
            print(f"Connection from {addr}")

            while True:
                msj = conn.recv(1024)
                if not msj:
                    break  # Rompe el bucle interno si el cliente cierra la conexión
                print(f"Mensaje: {msj.decode()}")
                if msj.decode().lower() == 'salir':
                    print("Closing server...")
                    conn.close()  # Cierra la conexión actual antes de detener el servidor
                    break  # Rompe el bucle while True para detener el servidor

            if not msj:
                break
            
            if msj.decode().lower() == 'salir':
                break  # Sale del bucle principal si se recibió el mensaje de 'salir'

    finally:
        server.close()  # Cierra el socket del servidor de manera adecuada
