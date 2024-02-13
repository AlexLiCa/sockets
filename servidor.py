
import socket as sk
import threading

# Diccionario para almacenar las conexiones de los clientes
client_connections = {}
client_addresses = {}


def client_thread(conn, addr):
    global client_connections
    client_id = addr[0] + ':' + str(addr[1])
    client_connections[client_id] = conn
    print(f"Conexión desde {addr} asignada a ID {client_id}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break  # Terminar bucle si no hay datos
            message = data.decode('utf-8')
            if message.startswith('@'):
                target_id, _, message_content = message[1:].partition(' ')
                # Enviar mensaje a un destinatario específico
                if target_id in client_connections:
                    client_connections[target_id].send(
                        f"Mensaje privado de {client_id}: {message_content}".encode('utf-8'))
                else:
                    conn.send(
                        f"Destinatario {target_id} no encontrado.".encode('utf-8'))
            else:
                # Enviar mensaje a todos menos al emisor
                for client, connection in client_connections.items():
                    if client != client_id:
                        connection.send(
                            f"{client_id}: {message}".encode('utf-8'))
    finally:
        conn.close()
        del client_connections[client_id]
        print(f"Conexión con {client_id} cerrada")


def main():
    server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    port = 1234
    host = sk.gethostname()
    try:
        server.bind((host, port))
    except sk.error as e:
        print(f"Error al bincular el socket: {e}")
        return False

    print(f"Servidor escuchando en: {host} : {port}")
    server.listen()

    try:
        while True:
            conn, addr = server.accept()
            client_id = addr[0] + ':' + str(addr[1])
            client_connections[client_id] = conn
            # Iniciar un nuevo hilo para manejar la conexión
            threading.Thread(target=client_thread, args=(conn, addr)).start()
    finally:
        server.close()


if __name__ == "__main__":
    main()
