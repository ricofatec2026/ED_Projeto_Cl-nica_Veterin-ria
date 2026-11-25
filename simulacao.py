"""
Simulacao de atendimento completo da Clinica Veterinaria.

Segue exatamente o fluxo pedido no enunciado:
    1. Chegada do animal e entrada na espera (normal ou emergencia).
    2. Chamada do proximo animal quando um consultorio fica livre e
       abertura do prontuario.
    3. Diagnostico na arvore de sistemas, marcando os itens alterados.
    4. Inclusao de medicamentos e procedimentos no prontuario, com
       baixa no estoque pelo lote mais antigo.
    5. Alta do animal, fechamento do prontuario e pagamento.

Integra os modulos:
    modelos/atendimento.py   -> ControleAtendimento (fila emergencia + fila normal)
    modelos/tutor.py          -> ControleTutores (tutores e animais)
    modelos/diagnostico.py    -> ControleDiagnostico (arvore de sistemas)
    modelos/estoque.py        -> ControleEstoque (lista de produtos + fila de lotes)
    modelos/prontuario.py     -> ControleProntuarios
    modelos/pagamento.py      -> ControleFinanceiro
    modelos/fechamento.py     -> ControleFechamento

Este arquivo e um complemento ao main.py (menu interativo): serve para
demonstrar o fluxo completo de forma rapida e repetivel, sem precisar
digitar os dados manualmente - util para gravacao de video ou testes
rapidos.
"""

from modelos.atendimento import ControleAtendimento, AnimalEspera
from modelos.tutor import ControleTutores, Tutor, Animal
from modelos.diagnostico import ControleDiagnostico
from modelos.estoque import ControleEstoque, Produto, Lote
from modelos.prontuario import ControleProntuarios, ItemMedicamento, ItemProcedimento
from modelos.pagamento import ControleFinanceiro
from modelos.fechamento import ControleFechamento


def preparar_cadastros():
    """Prepara os cadastros iniciais: tutores, animais e estoque de medicamentos."""
    controle_tutores = ControleTutores()
    controle_tutores.cadastrar_tutor(Tutor("Joao Silva", "111.111.111-11", "19999990000"))
    controle_tutores.cadastrar_animal("111.111.111-11", Animal("Rex", "Cachorro", "Labrador", 3))

    controle_estoque = ControleEstoque()

    vacina = Produto("Vacina antirrabica", "VAC001", "Fornecedor A", preco_venda=80.0, estoque_minimo=3)
    controle_estoque.cadastrar_produto(vacina)
    controle_estoque.adicionar_lote("VAC001", Lote("2026-09-01", 40.0, 5))
    controle_estoque.adicionar_lote("VAC001", Lote("2026-10-10", 42.0, 5))

    antibiotico = Produto("Amoxicilina", "ANT001", "Fornecedor B", preco_venda=45.0, estoque_minimo=2)
    controle_estoque.cadastrar_produto(antibiotico)
    controle_estoque.adicionar_lote("ANT001", Lote("2026-08-15", 20.0, 4))

    return controle_tutores, controle_estoque


def main():
    print("=" * 70)
    print("SIMULACAO DE ATENDIMENTO COMPLETO - CLINICA VETERINARIA")
    print("=" * 70)

    controle_tutores, controle_estoque = preparar_cadastros()
    controle_atendimento = ControleAtendimento()
    controle_prontuarios = ControleProntuarios()
    controle_financeiro = ControleFinanceiro()
    controle_fechamento = ControleFechamento(controle_estoque, controle_financeiro)

    # --- 1. Chegada do animal e entrada na espera ---
    print("\n[1] CHEGADA DO ANIMAL")
    animal_espera = AnimalEspera(
        nome_animal="Rex",
        nome_tutor="Joao Silva",
        data_hora_chegada="26/11 08:30",
        queixa="Vomito e falta de apetite",
        emergencia=False,
    )
    controle_atendimento.chegar_animal(animal_espera)
    print(f"  Animal {animal_espera.nome_animal} entrou na fila de espera (normal).")

    # --- 2. Chamada do proximo animal + abertura do prontuario ---
    print("\n[2] CONSULTORIO LIVRE -> CHAMANDO PROXIMO ANIMAL")
    proximo = controle_atendimento.proximo_animal()
    print(f"  Chamado: {proximo}")

    prontuario_atual = controle_prontuarios.abrir_prontuario(
        nome_animal=proximo.nome_animal,
        nome_tutor=proximo.nome_tutor,
        veterinario_responsavel="Dra. Ana",
        data_hora_abertura="26/11 08:35",
    )
    print(f"  {prontuario_atual}")

    # --- 3. Diagnostico na arvore de sistemas ---
    print("\n[3] DIAGNOSTICO (arvore de sistemas)")
    diagnostico = ControleDiagnostico()
    diagnostico.marcar_alterado("DIG001")  # Estomago alterado (compativel com vomito)
    print("  Arvore apos diagnostico:")
    diagnostico.exibir_diagnostico()

    itens_alterados = diagnostico.listar_itens_alterados()
    print("\n  Itens alterados encontrados no diagnostico:")
    for item in itens_alterados.percorrer():
        print(f"   -> {item.nome} ({item.codigo})")

    # --- 4. Inclusao de medicamentos e procedimentos no prontuario ---
    print("\n[4] INCLUSAO DE MEDICAMENTOS E PROCEDIMENTOS NO PRONTUARIO")
    prontuario_atual.adicionar_medicamento(ItemMedicamento("ANT001", "Amoxicilina", quantidade=2, preco_unitario=45.0))
    prontuario_atual.adicionar_procedimento(ItemProcedimento("Consulta veterinaria", 100.0))
    print(f"  Medicamentos: {list(prontuario_atual.medicamentos.percorrer())}")
    print(f"  Procedimentos: {list(prontuario_atual.procedimentos.percorrer())}")
    print(f"  Valor total parcial: R$ {prontuario_atual.valor_total():.2f}")

    print(f"\n  Estoque de Amoxicilina ANTES da baixa: {controle_estoque.buscar_produto('ANT001').quantidade_total()}")

    # --- 5. Alta, fechamento do prontuario e pagamento ---
    print("\n[5] ALTA, FECHAMENTO DO PRONTUARIO E PAGAMENTO")
    prontuario_atual.conceder_alta()
    pagamento, registro = controle_fechamento.fechar_prontuario_com_pagamento(
        prontuario=prontuario_atual,
        forma_pagamento="CARTAO",
        data_hora_pagamento="26/11 10:00",
        parcelas=2,
    )

    print(f"  {pagamento}")
    print(f"  {registro}")
    print(f"  Estoque de Amoxicilina APOS a baixa: {controle_estoque.buscar_produto('ANT001').quantidade_total()}")
    print(f"  Lotes consumidos (rastreabilidade): {list(registro.lotes_consumidos['ANT001'].percorrer())}")

    print("\n" + "=" * 70)
    print(f"Faturamento total da clinica: R$ {controle_financeiro.faturamento_total():.2f}")
    print("Simulacao concluida com sucesso.")
    print("=" * 70)


if __name__ == "__main__":
    main()
