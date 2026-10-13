import rpyc

HOST = "127.0.0.1"
PORTA = 18861

conexao = rpyc.connect(HOST, PORTA)
try:
    horario = conexao.root.obter_horario()  # chamada remota
    print(f"Horário do servidor: {horario}")
finally:
    conexao.close()