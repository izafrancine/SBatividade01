import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORTA = 8000


def atender_cliente(conn, endereco):
    """Executada em uma thread por cliente."""
    with conn:
        try:
            pedido = conn.recv(1024).decode("utf-8").strip()
            print(f"[{threading.current_thread().name}] Pedido de {endereco}: {pedido!r}")
            horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            conn.sendall(horario.encode("utf-8"))
        except OSError as erro:
            print(f"Erro com {endereco}: {erro}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORTA))
        servidor.listen()
        print(f"Servidor de horário escutando na porta {PORTA}...")

        while True:
            conn, endereco = servidor.accept()
            thread = threading.Thread(
                target=atender_cliente, args=(conn, endereco), daemon=True
            )
            thread.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")