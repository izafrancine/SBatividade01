import socket
import threading
import time

HOST = "0.0.0.0"
PORTA = 9000
LIMITE = 8          
INTERVALO_CHECK = 1  

ultimo_sinal = {}    
offline = set()      
trava = threading.Lock()


def checar_nos():
    """Thread de checagem periódica."""
    while True:
        time.sleep(INTERVALO_CHECK)
        agora = time.time()
        with trava:
            for no, instante in ultimo_sinal.items():
                if agora - instante > LIMITE and no not in offline:
                    offline.add(no)
                    print(f"[ALERTA] O Nó {no} está OFFLINE!")


def main():
    threading.Thread(target=checar_nos, daemon=True).start()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
        servidor.bind((HOST, PORTA))
        print(f"Monitor escutando heartbeats na porta {PORTA}...")

        while True:
            dados, _ = servidor.recvfrom(1024)
            partes = dados.decode("utf-8").split()
            if len(partes) != 2 or partes[0] != "PING":
                continue                      # ignora mensagens inválidas
            no = partes[1]

            with trava:
                if no not in ultimo_sinal:
                    print(f"Nó {no} registrado.")
                elif no in offline:
                    offline.discard(no)
                    print(f"[INFO] O Nó {no} voltou a ficar ONLINE.")
                ultimo_sinal[no] = time.time()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMonitor encerrado.")