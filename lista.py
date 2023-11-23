import json
from datetime import datetime, timedelta

exames_disponiveis = ["Perfil Lipídico", "Polissonografia", "Check-up Completo"]

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

dados = carregar_dados()

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
        print("6. Recomendar Exames Preventivos")
        print("7. Agendar exames")
        print("8. Sair")

        escolha = input("Digite o número da opção desejada: ")

        if escolha == "1":
            atividade = input("Digite sua média de tempo de exercícios na semana: ")
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
            agendar_exame(usuario_id)

        elif escolha == "8":
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

def visualizar_dados(usuario_id):
    usuario = obter_usuario_por_id(usuario_id)

    sono = calcular_media_sono(usuario)
    exercicios = calcular_media_exercicios(usuario)

    if sono < 7 and exercicios < 1:
        print("Recomendação: Aumente a prática de exercícios físicos (pelo menos 1 hora por dia) e melhore a qualidade do sono (alvo: 7 horas por noite).")
    elif sono < 7:
        print(f"Recomendação: Melhore a qualidade do sono (alvo: 7 horas por noite). Atual média de sono: {sono} horas.")
    elif exercicios < 1:
        print("Recomendação: Aumente a prática de exercícios físicos (pelo menos 1 hora por dia).")
    else:
        print("Ótimo trabalho! Continue assim.")

def calcular_media_sono(usuario):
    total_sono = sum(int(registro['duracao_sono']) for registro in usuario['padroes_de_sono'])
    return total_sono / len(usuario['padroes_de_sono']) if usuario['padroes_de_sono'] else 0

def calcular_media_exercicios(usuario):
    total_exercicios = sum(float(registro['atividade']) for registro in usuario['atividades'])
    return total_exercicios / len(usuario['atividades']) if usuario['atividades'] else 0


def obter_usuario_por_id(usuario_id):
    for usuario in dados['usuarios']:
        if usuario['id'] == usuario_id:
            return usuario
    return None

def registrar_atividade_fisica(usuario_id, atividade):
    usuario = obter_usuario_por_id(usuario_id)
    usuario['atividades'].append({'atividade': atividade, 'data': str(datetime.now())})
    salvar_dados(dados)
    print("Atividade física registrada com sucesso!")

def registrar_padrao_de_sono(usuario_id, duracao_sono):
    usuario = obter_usuario_por_id(usuario_id)
    usuario['padroes_de_sono'].append({'duracao_sono': duracao_sono, 'data': str(datetime.now())})
    salvar_dados(dados)
    print("Padrão de sono registrado com sucesso!")

def registrar_exame(usuario_id, tipo_exame):
    usuario = obter_usuario_por_id(usuario_id)
    usuario['exames'].append({'tipo_exame': tipo_exame, 'data': str(datetime.now())})
    salvar_dados(dados)

def visualizar_exames(usuario_id):
    usuario = obter_usuario_por_id(usuario_id)
    if 'exames' in usuario and len(usuario['exames']) > 0:
        print("Exames Registrados:")
        for exame in usuario['exames']:
            print(f"- {exame['tipo_exame']} em {exame['data']} ({calcular_tempo_decorrido(exame['data'])} atrás)")
    else:
        print("Nenhum exame registrado.")

def calcular_tempo_decorrido(data_exame_str):
    try:
        data_exame = datetime.strptime(data_exame_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        data_exame = datetime.strptime(data_exame_str, "%Y-%m-%d")

    tempo_decorrido = datetime.now() - data_exame
    dias_decorridos = tempo_decorrido.days
    if dias_decorridos == 0:
        segundos_decorridos = tempo_decorrido.seconds
        horas, segundos = divmod(segundos_decorridos, 3600)
        minutos, segundos = divmod(segundos, 60)
        return f"{horas} horas, {minutos} minutos e {segundos} segundos"
    elif dias_decorridos == 1:
        return "1 dia"
    else:
        return f"{dias_decorridos} dias, {tempo_decorrido.seconds // 3600} horas, {tempo_decorrido.seconds % 3600 // 60} minutos e {tempo_decorrido.seconds % 60} segundos"


def agendar_exame(usuario_id):
    print("\n=== Agendar Exame ===")
    print("Exames Disponíveis:")

    for i, exame in enumerate(exames_disponiveis, start=1):
        print(f"{i}. {exame}")

    try:
        opcao_exame = int(input("Escolha o número do exame desejado: "))

        if 1 <= opcao_exame <= len(exames_disponiveis):
            tipo_exame = exames_disponiveis[opcao_exame - 1]
            data_exame = input("Digite a data do exame (formato YYYY-MM-DD): ")

            if validar_data(data_exame):
                registrar_exame(usuario_id, tipo_exame)
                print(f"Exame de {tipo_exame} agendado com sucesso para {data_exame}.")
            else:
                print("Formato de data inválido. Use o formato YYYY-MM-DD.")
        else:
            print("Opção inválida. Escolha um número válido.")

    except ValueError:
        print("Opção inválida. Insira um número.")

def recomendar_exames_previos(usuario_id):
    usuario = obter_usuario_por_id(usuario_id)
    data_exame = None
    if 'exames' in usuario and len(usuario['exames']) > 0:
        data_exame = usuario['exames'][-1]['data']

    if data_exame is not None:
        data_exame = datetime.strptime(data_exame, "%Y-%m-%d %H:%M:%S.%f")
        tempo_decorrido = datetime.now() - data_exame
        dias_decorridos = tempo_decorrido.days
        sono = calcular_media_sono(usuario)
        exercicios = calcular_media_exercicios(usuario)

        if dias_decorridos > 90:
            print(f"Seu último exame foi realizado há {dias_decorridos} dias. Recomendamos que marque um Check-up Completo.")
        elif sono < 5:
            print(f"Recomendamos agendar uma Polissonografia, pelo seu baixo tempo de sono.")
        elif exercicios < 1:
            print(f"Recomendamos agendar um exame de Perfil Lipídico, pela baixa atividade física.")
        else:
            print("Seu último exame está dentro do período recomendado e seus dados de saúde parecem bons, não é necessário exame preventivo no momento. Continue assim!")
    else:
        print("Nenhum exame registrado. Recomendamos agendar um Check-up Completo para avaliação abrangente da sua saúde.")

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
