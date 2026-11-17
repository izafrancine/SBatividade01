import rpyc

HOST = "127.0.0.1"
PORTA = 18861


def mostrar_mapa(conexao):
    assentos = conexao.root.listar_assentos()
    print("\n=== MAPA DE ASSENTOS ===")
    for assento, status in assentos:
        marca = "[ ]" if status == "Livre" else "[X]"
        print(f"  {assento:<4} {marca} {status}")
    print("[ ] = livre   [X] = reservado")


def main():
    conexao = rpyc.connect(HOST, PORTA)
    nome = input("Seu nome: ").strip()

    try:
        while True:
            print("\n1) Ver mapa de assentos")
            print("2) Reservar assento")
            print("3) Sair")
            opcao = input("Escolha: ").strip()

            if opcao == "1":
                mostrar_mapa(conexao)
            elif opcao == "2":
                mostrar_mapa(conexao)
                assento = input("Qual assento deseja (ex: A3)? ")
                sucesso, mensagem = conexao.root.reservar_assento(nome, assento)
                print(("✔ " if sucesso else "✘ ") + mensagem)
            elif opcao == "3":
                break
            else:
                print("Opção inválida.")
    finally:
        conexao.close()
        print("Conexão encerrada.")


if __name__ == "__main__":
    main()