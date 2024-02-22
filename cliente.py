
import socket as sk
import threading
from prueba import mi_ip


def enviar_mensajes(sock):
    print("Conectado al servidor. Puedes enviar mensajes.")
    print("Usa '@nombre_destinatario mensaje' para enviar un mensaje privado.")
    print("Usa '/usuarios' para ver todos los usuarios en el server.")
    print("Usa '/agregar_amigo' para agregar a alguien a la lista de amigos.")
    print("Usa '/eliminar_amigo' para eliminar a alguien a la lista de amigos.")
    print("Usa '@amigos' y un mensaje para enviar un menaje a todos tus amigos.")
    print("Usa '/ver_amigos' para ver el estado de tus amigos.")
    print("Usa '/historial' para ver tu historial de mensajes.")
    print("Escribe solo el mensaje para enviarlo a todos los usuarios conectado.")
    while True:
        mensaje = input("")
        if mensaje.lower() == 'salir':
            break
        try:
            sock.send(mensaje.encode('utf-8'))
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            break


def recibir_mensajes(sock):
    while True:
        try:
            mensaje = sock.recv(1024).decode('utf-8')
            if mensaje:
                print("\nMensaje recibido:", mensaje)
            else:
                # El servidor cerró la conexión
                print("\nSe ha perdido la conexión con el servidor.")
                sock.close()
                break
        except Exception as e:
            print(f"\nError al recibir mensajes: {e}")
            sock.close()
            break


def main():
    cliente = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

    host = mi_ip
    port = 1234
    
    try:
        cliente.connect((host, port))
        #Enviamos el alias al servidor 
        alias = input("Ingresa tu alias: ")
        cliente.send(alias.encode('utf-8'))

        alias = cliente.recv(1024).decode('utf-8')

        if alias == "true":
            print("Conectado al servidor. Puedes comenzar a enviar mensajes.")
            mensaje = "/usuarios"
            cliente.send(mensaje.encode('utf-8'))

            thread_recivir = threading.Thread(
                target=recibir_mensajes, args=(cliente,))
            thread_envio = threading.Thread(
                target=enviar_mensajes, args=(cliente,))

            thread_recivir.start()
            thread_envio.start()

            thread_envio.join()

            print("Conexión con el servidor cerrada.")
        else: 
            print("Alias ya esta en uso")


    except Exception as e:
        print(f"No se pudo conectar al servidor: {e}")
    finally:
        print("Socket del cliente cerrado")
        cliente.close()


if __name__ == "__main__":
    main()
