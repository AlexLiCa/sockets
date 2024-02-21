
import socket as sk
import threading

# Diccionario para almacenar las conexiones de los clientes
client_info = {}


def broadcast_message(sender_alias, message):
    """
    Envia un mensaje a todos los usuarios conectados, excepto al remitente.

    :param sender_alias: El alias del remitente.
    :param message: El mensaje a enviar.
    """
    for alias, info in client_info.items():
        if alias != sender_alias:  # Evita enviar el mensaje al remitente
            try:
                # Obtiene la conexión de socket del destinatario
                conn = info["conn"]
                conn.send(f"{sender_alias}: {message}".encode('utf-8'))
            except Exception as e:
                print(f"Error al enviar mensaje a {alias}: {e}")

def client_thread(conn, alias):
    # alias = addr[0]
    client_data = client_info.get(alias, {"friends": [], "conn": conn})
    client_info[alias] = client_data
    print(f"Conexión de {alias} asignada a ID {alias}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            if message.startswith('@'):
                target_alias, _, message_content = message[1:].partition(' ')
                if target_alias in client_info and target_alias != alias:
                    # Accede a la conexión de socket del destinatario a través de 'conn'
                    client_info[target_alias]["conn"].send(
                        f"Mensaje privado de {alias}: {message_content}".encode('utf-8'))
                elif target_alias == alias:
                    conn.send(
                        f"Destinatario {target_alias} es usted.".encode('utf-8'))
                else:
                    conn.send(
                        f"Destinatario {target_alias} no encontrado.".encode('utf-8'))
            elif message.strip() == "/usuarios":
                usuarios = "\n".join(client_info.keys())
                conn.send(
                    f"Usuarios conectados:\n{usuarios}".encode('utf-8'))
            # -----------------------------------------------------------------------
            # Manejo de mensajes para amigos
            # -----------------------------------------------------------------------
            elif message.startswith("/agregar_amigo "):
                # Lógica para agregar amigo
                friend_ip = message.split(" ", 1)[1]
                if friend_ip not in client_data["friends"]:
                    client_data["friends"].append(friend_ip)
                    conn.send(
                        f"{friend_ip} añadido como amigo.".encode('utf-8'))
                else:
                    conn.send(f"{friend_ip} ya es tu amigo.".encode('utf-8'))
            elif message.startswith("/eliminar_amigo "):
                # Lógica para eliminar amigo
                friend_ip = message.split(" ", 1)[1]
                if friend_ip in client_data["friends"]:
                    client_data["friends"].remove(friend_ip)
                    conn.send(
                        f"{friend_ip} eliminado de tus amigos.".encode('utf-8'))
                else:
                    conn.send(
                        f"{friend_ip} no está en tu lista de amigos.".encode('utf-8'))
            elif message.startswith("/amigos"):
                _, _, friend_message = message.partition(' ')  
                amigos_conectados = 0
                for friend_alias in client_data["friends"]:
                    if friend_alias in client_info:  
                        client_info[friend_alias]["conn"].send(
                            f"Mensaje de {alias} (Amigo): {friend_message}".encode('utf-8'))
                        amigos_conectados += 1
                if amigos_conectados == 0: 
                    conn.send(
                        "Ninguno de tus amigos está en línea.".encode('utf-8'))
            elif message == "/ver_amigos":
                # Lógica para ver el estado de los amigos
                friends_status = "\n".join(
                    [f"{friend_ip} {'en línea' if friend_ip in client_info else 'fuera de línea'}" for friend_ip in client_data["friends"]])
                conn.send(
                    f"Estado de amigos:\n{friends_status}".encode('utf-8'))
            else:
                broadcast_message(alias, message)
    finally:
        conn.close()
        del client_info[alias]
        print(f"Conexión con {alias} cerrada")


def main():
    server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    port = 1234
    host = "172.18.16.3"
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
            alias = conn.recv(1024).decode('utf-8')
            if alias not in client_info:
                # Inicializa un nuevo registro para el alias si no existe previamente
                client_info[alias] = {"conn": conn, "friends": []}
            else:
                # Actualiza la conexión en caso de reconexión, mantener amigos existentes
                client_info[alias]["conn"] = conn
                client_info[alias] = conn
                # Iniciar un nuevo hilo para manejar la conexión
            threading.Thread(target=client_thread, args=(conn, alias)).start()
    finally:
        server.close()


if __name__ == "__main__":
    main()
