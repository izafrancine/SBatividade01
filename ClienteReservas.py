import threading

import rpyc
from rpyc.utils.server import ThreadedServer

HOST = "0.0.0.0"
PORTA = 18861

# Estado compartilhado: assento -> nome de quem reservou (None = livre)
assentos = {f"A{i}": None for i in range(1, 11)}
trava = threading.Lock()


class ServicoReservas(rpyc.Service):
    def on_connect(self, conn):
        print("Cliente conectado.")

    def on_disconnect(self, conn):
        print("Cliente desconectado.")

    def exposed_listar_assentos(self):
        """Retorna ((assento, status), ...) com status 'Livre' ou 'Reservado'."""
        with trava:
            return tuple(
                (assento, "Livre" if dono is None else "Reservado")
                for assento, dono in assentos.items()
            )

    def exposed_reservar_assento(self, nome_cliente, assento):
        """Tenta reservar o assento. Retorna (sucesso, mensagem)."""
        assento = assento.strip().upper()
        nome_cliente = nome_cliente.strip()

        if not nome_cliente:
            return (False, "Informe um nome válido.")

        # Seção crítica: verificar e reservar precisam ser uma operação única.
        with trava:
            if assento not in assentos:
                return (False, f"Assento {assento} não existe.")
            if assentos[assento] is not None:
                print(f"{nome_cliente} tentou {assento}: já ocupado.")
                return (False, f"Assento {assento} já ocupado.")
            assentos[assento] = nome_cliente
            print(f"{nome_cliente} reservou {assento}.")
            return (True, f"Assento {assento} reservado para {nome_cliente}!")


if __name__ == "__main__":
    servidor = ThreadedServer(ServicoReservas, hostname=HOST, port=PORTA)
    print(f"Servidor de reservas escutando na porta {PORTA}...")
    try:
        servidor.start()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")