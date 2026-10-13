from datetime import datetime

import rpyc
from rpyc.utils.server import ThreadedServer

HOST = "0.0.0.0"
PORTA = 18861  


class ServicoHorario(rpyc.Service):
    def on_connect(self, conn):
        print("Cliente conectado.")

    def on_disconnect(self, conn):
        print("Cliente desconectado.")

    def exposed_obter_horario(self):
        """Procedimento remoto: retorna o horário atual do servidor."""
        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"Horário solicitado. Retornando: {horario}")
        return horario


if __name__ == "__main__":
    servidor = ThreadedServer(ServicoHorario, hostname=HOST, port=PORTA)
    print(f"Servidor RPyC escutando na porta {PORTA}...")
    try:
        servidor.start()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")