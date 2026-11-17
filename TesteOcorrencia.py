import threading

import rpyc

HOST, PORTA = "127.0.0.1", 18861
ASSENTO = "A5"
N_CLIENTES = 8

largada = threading.Barrier(N_CLIENTES)   # todos disparam juntos
resultados = []


def cliente(nome):
    conexao = rpyc.connect(HOST, PORTA)
    largada.wait()
    resultados.append((nome, *conexao.root.reservar_assento(nome, ASSENTO)))
    conexao.close()


threads = [threading.Thread(target=cliente, args=(f"Cliente_{i}",)) for i in range(1, N_CLIENTES + 1)]
for t in threads: t.start()
for t in threads: t.join()

for nome, ok, msg in sorted(resultados):
    print(f"{nome}: {'SUCESSO' if ok else 'FALHOU '} - {msg}")
print(f"\nTotal de sucessos: {sum(r[1] for r in resultados)} (esperado: 1)")