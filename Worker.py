import socket
import sys
import time

HOST = "127.0.0.1"
PORTA = 9000
INTERVALO = 3   

id_no = sys.argv[1] if len(sys.argv) > 1 else input("ID do nó (ex: Worker_1): ")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    print(f"{id_no} enviando heartbeat a cada {INTERVALO}s (Ctrl+C para parar)...")
    try:
        while True:
            sock.sendto(f"PING {id_no}".encode("utf-8"), (HOST, PORTA))
            print(f"PING enviado ({time.strftime('%H:%M:%S')})")
            time.sleep(INTERVALO)
    except KeyboardInterrupt:
        print(f"\n{id_no} encerrado.")