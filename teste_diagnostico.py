"""
Testes manuais do Diagnostico (Arvore de Sistemas do Animal).
Rodar com: python -m testes.teste_diagnostico (a partir da raiz do projeto)
"""

from modelos.diagnostico import ControleDiagnostico


def testar_marcacao_alterado():
    print("== Marcando itens alterados ==")
    d = ControleDiagnostico()
    d.marcar_alterado("DIG001")  # Estomago
    d.marcar_alterado("RES002")  # Traqueia
    d.exibir_diagnostico()

    itens = list(d.listar_itens_alterados().percorrer())
    print("\nTotal de itens alterados:", len(itens))
    assert len(itens) == 2


def testar_codigo_invalido():
    print("\n== Codigo invalido (deve lancar erro) ==")
    d = ControleDiagnostico()
    try:
        d.marcar_alterado("CODIGO_INEXISTENTE")
        print("ERRO: deveria ter lancado excecao!")
    except ValueError as e:
        print("Excecao esperada capturada:", e)


def testar_reverter_estado():
    print("\n== Marcar alterado e depois reverter para saudavel ==")
    d = ControleDiagnostico()
    d.marcar_alterado("PEL001")
    assert len(list(d.listar_itens_alterados().percorrer())) == 1
    d.marcar_saudavel("PEL001")
    assert len(list(d.listar_itens_alterados().percorrer())) == 0
    print("Reversao funcionou corretamente")


if __name__ == "__main__":
    testar_marcacao_alterado()
    testar_codigo_invalido()
    testar_reverter_estado()
    print("\nTodos os testes passaram.")
