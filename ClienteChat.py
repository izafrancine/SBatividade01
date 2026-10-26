import socket
import threading

HOST = "127.0.0.1"
PORTA = 8000


def receber(sock):
    """Fica escutando o servidor e imprimindo as mensagens."""
    while True:
        try:
            dados = sock.recv(1024).decode("utf-8")
        except OSError:
            break
        if not dados:
            print("Conexão com o servidor encerrada.")
            break
        print(dados)


nome = input("Seu nome: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORTA))
sock.sendall(nome.encode("utf-8"))

threading.Thread(target=receber, args=(sock,), daemon=True).start()

print("Conectado! Digite suas mensagens (digite 'sair' para encerrar).")
while True:
    mensagem = input()
    if mensagem.lower() == "sair":
        break
    sock.sendall(mensagem.encode("utf-8"))

sock.close()