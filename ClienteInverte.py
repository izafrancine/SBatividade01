"""Item 2 - Cliente: envia uma string e exibe a resposta invertida."""
import socket

HOST = "127.0.0.1"
PORTA = 8000
MENSAGEM = "Olá Mundo Distribuído"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORTA))
    cliente.sendall(MENSAGEM.encode("utf-8"))
    resposta = cliente.recv(1024).decode("utf-8")
    print(f"Enviado:  {MENSAGEM}")
    print(f"Recebido: {resposta}")