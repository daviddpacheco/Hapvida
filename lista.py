import json
from datetime import datetime

credenciais = {'usuario': 'fiap', 'senha': '123'}

exames_Codisponiveis = ["Hemograma", "lesterol Total", "Glicose", "Urina Tipo I", "Check-up Completo"]

def carregar_dados():
    try:
        with open('dados.json', 'r') as arquivo:
            dados = json.load(arquivo)
            if not isinstance(dados.get('usuarios'), list):
                dados['usuarios'] = []
    except FileNotFoundError:
        dados = {'usuarios': []}
    return dados

def salvar_dados(dados):
    with open('dados.json', 'w') as arquivo:
        json.dump(dados, arquivo, indent=2)

dados = carregar_dados()  # Torna dados uma variável global

def validar_data(data_str):
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def menu_usuario(usuario_id):
    while True:
        print("\n=== Menu ===")
        print("1. Registrar Atividade Física")
        print("2. Registrar Padrão de Sono")
        print("3. Visualizar Dados de Saúde")
        print("4. Registrar Exame")
        print("5. Visualizar Exames")
        print("6. Recomendar Exames Prévios")
        print("7. Sair")

        escolha = input("Digite o número da opção desejada: ")

        if escolha == "1":
            atividade = input("Digite a atividade física realizada: ")
            registrar_atividade_fisica(usuario_id, atividade)

        elif escolha == "2":
            duracao_sono = input("Digite a duração do sono em horas: ")
            registrar_padrao_de_sono(usuario_id, duracao_sono)

        elif escolha == "3":
            visualizar_dados(usuario_id)

        elif escolha == "4":
            tipo_exame = input("Digite o tipo de exame realizado: ")
            registrar_exame(usuario_id, tipo_exame)

        elif escolha == "5":
            visualizar_exames(usuario_id)

        elif escolha == "6":
            recomendar_exames_previos(usuario_id)

        elif escolha == "7":
            print("Saindo do sistema. Até logo!")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

def criar_conta():
    novo_usuario = {
        "id": str(len(dados['usuarios']) + 1),
        "usuario": input("Digite um nome de usuário: "),
        "senha": input("Digite uma senha: "),
        "atividades": [],
        "padroes_de_sono": [],
        "exames": []
    }
    dados['usuarios'].append(novo_usuario)
    salvar_dados(dados)
    print("Conta criada com sucesso!")

def login():
    tentativas = 3
    while tentativas > 0:
        usuario_digitado = input("Digite seu usuário: ")
        senha_digitada = input("Digite sua senha: ")

        for usuario in dados['usuarios']:
            if usuario['usuario'] == usuario_digitado and usuario['senha'] == senha_digitada:
                print("Login bem-sucedido!")
                return usuario['id']

        tentativas -= 1
        print(f"Login falhou. Tentativas restantes: {tentativas}")

    print("Número de tentativas excedido. Saindo do sistema.")
    return None

if __name__ == "__main__":

    while True:
        print("\n=== Menu Inicial ===")
        print("1. Login")
        print("2. Criar Conta")
        print("3. Sair")

        escolha = input("Digite o número da opção desejada: ")

        if escolha == "1":
            usuario_id = login()
            if usuario_id:
                menu_usuario(usuario_id)
            else:
                break

        elif escolha == "2":
            criar_conta()

        elif escolha == "3":
            print("Saindo do sistema. Até logo!")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
