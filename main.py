"""
Menu interativo da Clinica Veterinaria.

Permite ao usuario inserir dados manualmente, cobrindo o fluxo
completo pedido no enunciado:
    1. Cadastro de tutores e animais
    2. Chegada do animal e entrada na espera (normal ou emergencia)
    3. Chamada do proximo animal e abertura do prontuario
    4. Diagnostico na arvore de sistemas, marcando itens alterados
    5. Cadastro de produtos e lotes no estoque
    6. Inclusao de medicamentos e procedimentos no prontuario
    7. Alta, fechamento do prontuario (com baixa de estoque) e pagamento

Integra os modulos:
    estruturas/      -> Lista, Fila, Pilha, Arvore (genericas)
    modelos/atendimento.py   -> ControleAtendimento (fila emergencia + fila normal)
    modelos/tutor.py          -> ControleTutores (lista de tutores + lista de animais)
    modelos/diagnostico.py    -> ControleDiagnostico (arvore de sistemas)
    modelos/estoque.py        -> ControleEstoque (lista de produtos + fila de lotes)
    modelos/prontuario.py     -> ControleProntuarios
    modelos/pagamento.py      -> ControleFinanceiro
    modelos/fechamento.py     -> ControleFechamento (orquestra o fechamento)
"""

from modelos.atendimento import ControleAtendimento, AnimalEspera
from modelos.tutor import ControleTutores, Tutor, Animal
from modelos.diagnostico import ControleDiagnostico
from modelos.estoque import ControleEstoque, Produto, Lote
from modelos.prontuario import ControleProntuarios, ItemMedicamento, ItemProcedimento
from modelos.pagamento import ControleFinanceiro
from modelos.fechamento import ControleFechamento


class SistemaClinica:
    """Agrupa todos os controles do sistema, compartilhados entre as telas do menu."""

    def __init__(self):
        self.controle_tutores = ControleTutores()
        self.controle_atendimento = ControleAtendimento()
        self.controle_estoque = ControleEstoque()
        self.controle_prontuarios = ControleProntuarios()
        self.controle_financeiro = ControleFinanceiro()
        self.controle_fechamento = ControleFechamento(self.controle_estoque, self.controle_financeiro)

        # dicionario simples (apenas no main, fora das estruturas do problema)
        # para lembrar o diagnostico (arvore) de cada prontuario aberto
        self._diagnosticos_por_prontuario = {}


def ler_float(mensagem, padrao=None):
    """Le um numero decimal do usuario, com valor padrao opcional."""
    while True:
        entrada = input(mensagem).strip()
        if entrada == "" and padrao is not None:
            return padrao
        try:
            return float(entrada)
        except ValueError:
            print("  Valor invalido, digite um numero (ex.: 10.50).")


def ler_int(mensagem, padrao=None):
    """Le um numero inteiro do usuario, com valor padrao opcional."""
    while True:
        entrada = input(mensagem).strip()
        if entrada == "" and padrao is not None:
            return padrao
        try:
            return int(entrada)
        except ValueError:
            print("  Valor invalido, digite um numero inteiro.")


def ler_sim_nao(mensagem):
    """Le uma resposta sim/nao do usuario."""
    while True:
        entrada = input(mensagem + " (s/n): ").strip().lower()
        if entrada in ("s", "sim"):
            return True
        if entrada in ("n", "nao", "não"):
            return False
        print("  Responda com 's' ou 'n'.")


# ---------------------------------------------------------------------
# 1. Tutores e Animais
# ---------------------------------------------------------------------

def menu_cadastrar_tutor(sistema: SistemaClinica):
    print("\n--- Cadastrar Tutor ---")
    nome = input("Nome do tutor: ").strip()
    cpf = input("CPF: ").strip()
    telefone = input("Telefone: ").strip()
    try:
        sistema.controle_tutores.cadastrar_tutor(Tutor(nome, cpf, telefone))
        print(f"Tutor '{nome}' cadastrado com sucesso.")
    except ValueError as e:
        print("Erro:", e)


def menu_cadastrar_animal(sistema: SistemaClinica):
    print("\n--- Cadastrar Animal ---")
    cpf = input("CPF do tutor: ").strip()
    nome = input("Nome do animal: ").strip()
    especie = input("Especie (ex.: Cachorro, Gato): ").strip()
    raca = input("Raca: ").strip()
    idade = ler_int("Idade (anos): ", padrao=0)
    try:
        sistema.controle_tutores.cadastrar_animal(cpf, Animal(nome, especie, raca, idade))
        print(f"Animal '{nome}' cadastrado para o tutor de CPF {cpf}.")
    except ValueError as e:
        print("Erro:", e)


def menu_buscar_animal(sistema: SistemaClinica):
    print("\n--- Buscar Animal (por nome + CPF do tutor) ---")
    cpf = input("CPF do tutor: ").strip()
    nome = input("Nome do animal: ").strip()
    tutor, animal = sistema.controle_tutores.buscar_animal_por_nome_e_cpf(cpf, nome)
    if animal is None:
        print("Animal nao encontrado.")
    else:
        print(f"Encontrado: {animal} | Tutor: {tutor.nome}")


def menu_listar_tutores(sistema: SistemaClinica):
    print("\n--- Tutores cadastrados ---")
    if sistema.controle_tutores.tutores.esta_vazia():
        print("Nenhum tutor cadastrado.")
        return
    for tutor in sistema.controle_tutores.tutores.percorrer():
        print(f"- {tutor}")
        for animal in tutor.animais.percorrer():
            print(f"    -> {animal}")


# ---------------------------------------------------------------------
# 2 e 3. Atendimento (fila de espera + chamada + abertura de prontuario)
# ---------------------------------------------------------------------

def menu_chegada_animal(sistema: SistemaClinica):
    print("\n--- Chegada de Animal (entrada na espera) ---")
    nome_animal = input("Nome do animal: ").strip()
    nome_tutor = input("Nome do tutor: ").strip()
    data_hora = input("Data/hora de chegada (ex.: 26/11 09:00): ").strip()
    queixa = input("Queixa relatada: ").strip()
    emergencia = ler_sim_nao("E um caso de emergencia?")

    animal_espera = AnimalEspera(nome_animal, nome_tutor, data_hora, queixa, emergencia)
    sistema.controle_atendimento.chegar_animal(animal_espera)
    print(f"'{nome_animal}' entrou na fila de espera ({'emergencia' if emergencia else 'normal'}).")


def menu_chamar_proximo(sistema: SistemaClinica):
    print("\n--- Consultorio livre: chamar proximo animal ---")
    if sistema.controle_atendimento.esta_vazia():
        print("Nao ha animais na fila de espera.")
        return

    proximo = sistema.controle_atendimento.proximo_animal()
    print(f"Chamado: {proximo}")

    veterinario = input("Veterinario responsavel: ").strip()
    data_hora_abertura = input("Data/hora de abertura do prontuario: ").strip()

    prontuario = sistema.controle_prontuarios.abrir_prontuario(
        nome_animal=proximo.nome_animal,
        nome_tutor=proximo.nome_tutor,
        veterinario_responsavel=veterinario,
        data_hora_abertura=data_hora_abertura,
    )
    sistema._diagnosticos_por_prontuario[prontuario.numero] = ControleDiagnostico()
    print(f"Prontuario aberto: {prontuario}")


# ---------------------------------------------------------------------
# 4. Diagnostico (arvore de sistemas)
# ---------------------------------------------------------------------

def menu_diagnostico(sistema: SistemaClinica):
    print("\n--- Diagnostico (Arvore de Sistemas) ---")
    numero = ler_int("Numero do prontuario: ")
    diagnostico = sistema._diagnosticos_por_prontuario.get(numero)
    if diagnostico is None:
        print("Prontuario nao encontrado ou nao possui diagnostico associado.")
        return

    print("\nArvore de sistemas atual:")
    diagnostico.exibir_diagnostico()

    codigo = input("\nCodigo do item a marcar como Alterado (ou ENTER para nao marcar): ").strip()
    if codigo:
        try:
            diagnostico.marcar_alterado(codigo)
            print(f"Item {codigo} marcado como Alterado.")
        except ValueError as e:
            print("Erro:", e)


# ---------------------------------------------------------------------
# 5. Estoque
# ---------------------------------------------------------------------

def menu_cadastrar_produto(sistema: SistemaClinica):
    print("\n--- Cadastrar Produto no Estoque ---")
    nome = input("Nome do produto: ").strip()
    codigo = input("Codigo: ").strip()
    fornecedor = input("Fornecedor: ").strip()
    preco_venda = ler_float("Preco de venda: R$ ")
    estoque_minimo = ler_int("Estoque minimo (ENTER para 0): ", padrao=0)
    try:
        sistema.controle_estoque.cadastrar_produto(
            Produto(nome, codigo, fornecedor, preco_venda, estoque_minimo)
        )
        print(f"Produto '{nome}' cadastrado.")
    except ValueError as e:
        print("Erro:", e)


def menu_adicionar_lote(sistema: SistemaClinica):
    print("\n--- Adicionar Lote ---")
    codigo = input("Codigo do produto: ").strip()
    data_compra = input("Data da compra (ex.: 2026-11-26): ").strip()
    preco_compra = ler_float("Preco de compra: R$ ")
    quantidade = ler_int("Quantidade: ")
    data_validade = input("Data de validade (ENTER se nao houver): ").strip() or None
    try:
        sistema.controle_estoque.adicionar_lote(
            codigo, Lote(data_compra, preco_compra, quantidade, data_validade)
        )
        print("Lote adicionado com sucesso.")
    except ValueError as e:
        print("Erro:", e)


def menu_listar_estoque(sistema: SistemaClinica):
    print("\n--- Estoque atual ---")
    if sistema.controle_estoque.produtos.esta_vazia():
        print("Nenhum produto cadastrado.")
        return
    for produto in sistema.controle_estoque.produtos.percorrer():
        print(f"- {produto}")


# ---------------------------------------------------------------------
# 6. Medicamentos e procedimentos no prontuario
# ---------------------------------------------------------------------

def menu_adicionar_medicamento(sistema: SistemaClinica):
    print("\n--- Adicionar Medicamento ao Prontuario ---")
    numero = ler_int("Numero do prontuario: ")
    prontuario = sistema.controle_prontuarios.buscar_por_numero(numero)
    if prontuario is None:
        print("Prontuario nao encontrado.")
        return

    codigo = input("Codigo do produto (estoque): ").strip()
    produto = sistema.controle_estoque.buscar_produto(codigo)
    if produto is None:
        print("Produto nao encontrado no estoque.")
        return

    quantidade = ler_int("Quantidade utilizada: ")
    try:
        prontuario.adicionar_medicamento(
            ItemMedicamento(codigo, produto.nome, quantidade, produto.preco_venda)
        )
        print(f"Medicamento '{produto.nome}' adicionado ao prontuario #{numero}.")
    except ValueError as e:
        print("Erro:", e)


def menu_adicionar_procedimento(sistema: SistemaClinica):
    print("\n--- Adicionar Procedimento ao Prontuario ---")
    numero = ler_int("Numero do prontuario: ")
    prontuario = sistema.controle_prontuarios.buscar_por_numero(numero)
    if prontuario is None:
        print("Prontuario nao encontrado.")
        return

    descricao = input("Descricao do procedimento (ex.: Consulta, Vacina, Curativo): ").strip()
    valor = ler_float("Valor: R$ ")
    try:
        prontuario.adicionar_procedimento(ItemProcedimento(descricao, valor))
        print(f"Procedimento '{descricao}' adicionado ao prontuario #{numero}.")
    except ValueError as e:
        print("Erro:", e)


def menu_ver_prontuario(sistema: SistemaClinica):
    print("\n--- Ver Prontuario ---")
    numero = ler_int("Numero do prontuario: ")
    prontuario = sistema.controle_prontuarios.buscar_por_numero(numero)
    if prontuario is None:
        print("Prontuario nao encontrado.")
        return
    print(prontuario)
    print("Medicamentos:", list(prontuario.medicamentos.percorrer()))
    print("Procedimentos:", list(prontuario.procedimentos.percorrer()))


# ---------------------------------------------------------------------
# 7. Alta, fechamento e pagamento
# ---------------------------------------------------------------------

def menu_fechar_prontuario(sistema: SistemaClinica):
    print("\n--- Alta, Fechamento e Pagamento ---")
    numero = ler_int("Numero do prontuario: ")
    prontuario = sistema.controle_prontuarios.buscar_por_numero(numero)
    if prontuario is None:
        print("Prontuario nao encontrado.")
        return

    if not prontuario.alta_concedida:
        if ler_sim_nao("Conceder alta ao animal agora?"):
            prontuario.conceder_alta()
        else:
            print("Fechamento cancelado: alta nao concedida.")
            return

    print("\nFormas de pagamento: PIX, CARTAO, DINHEIRO")
    forma = input("Forma de pagamento: ").strip().upper()
    parcelas = 1
    if forma == "CARTAO":
        parcelas = ler_int("Numero de parcelas: ", padrao=1)
    data_hora_pagamento = input("Data/hora do pagamento: ").strip()

    try:
        pagamento, registro = sistema.controle_fechamento.fechar_prontuario_com_pagamento(
            prontuario, forma, data_hora_pagamento, parcelas
        )
        print("\nProntuario fechado com sucesso!")
        print(pagamento)
        print(registro)
    except ValueError as e:
        print("Erro:", e)


def menu_faturamento(sistema: SistemaClinica):
    print("\n--- Faturamento Total ---")
    print(f"R$ {sistema.controle_financeiro.faturamento_total():.2f}")


# ---------------------------------------------------------------------
# Menu principal
# ---------------------------------------------------------------------

OPCOES = {
    "1": ("Cadastrar tutor", menu_cadastrar_tutor),
    "2": ("Cadastrar animal", menu_cadastrar_animal),
    "3": ("Buscar animal (nome + CPF do tutor)", menu_buscar_animal),
    "4": ("Listar tutores e animais", menu_listar_tutores),
    "5": ("Chegada de animal (entrar na fila de espera)", menu_chegada_animal),
    "6": ("Chamar proximo animal (consultorio livre)", menu_chamar_proximo),
    "7": ("Diagnostico (arvore de sistemas)", menu_diagnostico),
    "8": ("Cadastrar produto no estoque", menu_cadastrar_produto),
    "9": ("Adicionar lote ao estoque", menu_adicionar_lote),
    "10": ("Listar estoque", menu_listar_estoque),
    "11": ("Adicionar medicamento ao prontuario", menu_adicionar_medicamento),
    "12": ("Adicionar procedimento ao prontuario", menu_adicionar_procedimento),
    "13": ("Ver prontuario", menu_ver_prontuario),
    "14": ("Alta, fechamento e pagamento", menu_fechar_prontuario),
    "15": ("Ver faturamento total", menu_faturamento),
    "0": ("Sair", None),
}


def exibir_menu():
    print("\n" + "=" * 50)
    print("CLINICA VETERINARIA - MENU PRINCIPAL")
    print("=" * 50)
    for chave, (descricao, _) in OPCOES.items():
        print(f"{chave}. {descricao}")


def main():
    sistema = SistemaClinica()

    while True:
        exibir_menu()
        escolha = input("\nEscolha uma opcao: ").strip()

        if escolha == "0":
            print("Encerrando o sistema. Ate mais!")
            break

        opcao = OPCOES.get(escolha)
        if opcao is None:
            print("Opcao invalida, tente novamente.")
            continue

        _, funcao = opcao
        funcao(sistema)


if __name__ == "__main__":
    main()
