import socket

HOST = "127.0.0.1"
PORTA = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
    cliente.connect((HOST, PORTA))
    cliente.sendall("HORARIO".encode("utf-8"))
    horario = cliente.recv(1024).decode("utf-8")
    print(f"Horário do servidor: {horario}")