"""
Testes manuais do Prontuario de Atendimento.
Rodar com: python -m testes.teste_prontuario (a partir da raiz do projeto)
"""

from modelos.prontuario import ControleProntuarios, ItemMedicamento, ItemProcedimento


def testar_fluxo_completo():
    print("== Fluxo completo: abrir, adicionar, remover, fechar ==")
    controle = ControleProntuarios()
    p1 = controle.abrir_prontuario("Mia", "Maria Souza", "Dr. Bruno", "26/11 10:00")

    p1.adicionar_medicamento(ItemMedicamento("ANT001", "Amoxicilina", 2, 45.0))
    p1.adicionar_procedimento(ItemProcedimento("Curativo", 70.0))

    print("Total antes do fechamento:", p1.valor_total())
    assert p1.valor_total() == 160.0

    p1.conceder_alta()
    p1.fechar()
    assert p1.fechado is True
    print("Prontuario fechado com sucesso:", p1)


def testar_bloqueio_apos_fechamento():
    print("\n== Bloqueio de edicao apos fechamento (deve lancar erro) ==")
    controle = ControleProntuarios()
    p1 = controle.abrir_prontuario("Tom", "Pedro Costa", "Dr. Bruno", "26/11 11:00")
    p1.conceder_alta()
    p1.fechar()

    try:
        p1.adicionar_procedimento(ItemProcedimento("Vacina", 50.0))
        print("ERRO: deveria ter lancado excecao!")
    except ValueError as e:
        print("Excecao esperada capturada:", e)


def testar_busca_por_animal():
    print("\n== Busca de prontuario aberto por animal ==")
    controle = ControleProntuarios()
    controle.abrir_prontuario("Bidu", "Cliente A", "Dr. C", "26/11 08:00")
    encontrado = controle.buscar_por_animal("Bidu")
    print("Prontuario encontrado:", encontrado)
    assert encontrado is not None


if __name__ == "__main__":
    testar_fluxo_completo()
    testar_bloqueio_apos_fechamento()
    testar_busca_por_animal()
    print("\nTodos os testes passaram.")
