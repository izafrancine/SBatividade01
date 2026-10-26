import socket
import threading

HOST = "0.0.0.0"
PORTA = 8000

clientes = []                 # sockets dos clientes conectados
trava = threading.Lock()      # protege a lista entre as threads


def transmitir(mensagem, remetente=None):
    """Envia a mensagem a todos os clientes, menos ao remetente."""
    with trava:
        for c in clientes:
            if c is not remetente:
                try:
                    c.sendall(mensagem.encode("utf-8"))
                except OSError:
                    pass


def atender_cliente(conn):
    try:
        nome = conn.recv(1024).decode("utf-8").strip()
        print(f"{nome} entrou no chat.")
        transmitir(f"*** {nome} entrou no chat ***", conn)

        while True:
            dados = conn.recv(1024).decode("utf-8")
            if not dados:          # cliente fechou a conexão
                break
            print(f"{nome}: {dados}")
            transmitir(f"{nome}: {dados}", conn)
    except OSError:
        pass
    finally:
        with trava:
            if conn in clientes:
                clientes.remove(conn)
        conn.close()
        print(f"{nome} saiu do chat.")
        transmitir(f"*** {nome} saiu do chat ***")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORTA))
        servidor.listen()
        print(f"Servidor de chat escutando na porta {PORTA}...")

        while True:
            conn, _ = servidor.accept()
            with trava:
                clientes.append(conn)
            threading.Thread(target=atender_cliente, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")