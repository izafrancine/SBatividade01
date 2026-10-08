import socket
import threading

HOST = "0.0.0.0"
PORTA = 8000


def atender_cliente(conn, endereco):
    with conn:
        try:
            dados = conn.recv(1024).decode("utf-8")
            print(f"Recebido de {endereco}: {dados!r}")
            invertida = dados[::-1]
            conn.sendall(invertida.encode("utf-8"))
            print(f"Enviado: {invertida!r}")
        except OSError as erro:
            print(f"Erro com {endereco}: {erro}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORTA))
        servidor.listen()
        print(f"Servidor de inversão escutando na porta {PORTA}...")

        while True:
            conn, endereco = servidor.accept()
            threading.Thread(
                target=atender_cliente, args=(conn, endereco), daemon=True
            ).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")