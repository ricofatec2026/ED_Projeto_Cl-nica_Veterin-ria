"""
Testes manuais do Controle de Estoque.
Rodar com: python -m testes.teste_estoque (a partir da raiz do projeto)
"""

from modelos.estoque import ControleEstoque, Produto, Lote


def testar_baixa_fifo():
    print("== Baixa consome lote mais antigo primeiro (FIFO) ==")
    controle = ControleEstoque()
    antibiotico = Produto("Amoxicilina", "ANT001", "Fornecedor B", preco_venda=45.0, estoque_minimo=10)
    controle.cadastrar_produto(antibiotico)
    controle.adicionar_lote("ANT001", Lote("2026-08-01", 20.0, 15))
    controle.adicionar_lote("ANT001", Lote("2026-09-15", 22.0, 10))

    consumidos = controle.baixar_estoque("ANT001", 18)
    for lote in consumidos.percorrer():
        print(" consumido:", lote)
    print("Restante:", antibiotico.quantidade_total())
    assert antibiotico.quantidade_total() == 7


def testar_alerta_minimo():
    print("\n== Alerta de estoque abaixo do minimo ==")
    controle = ControleEstoque()
    vermifugo = Produto("Vermifugo", "VER001", "Fornecedor C", preco_venda=30.0, estoque_minimo=5)
    controle.cadastrar_produto(vermifugo)
    controle.adicionar_lote("VER001", Lote("2026-09-01", 10.0, 6))

    controle.baixar_estoque("VER001", 3)
    print("Produtos abaixo do minimo:", list(controle.produtos_abaixo_do_minimo().percorrer()))


def testar_estoque_insuficiente():
    print("\n== Estoque insuficiente (deve lancar erro) ==")
    controle = ControleEstoque()
    vacina = Produto("Vacina V10", "VAC002", "Fornecedor D", preco_venda=90.0)
    controle.cadastrar_produto(vacina)
    controle.adicionar_lote("VAC002", Lote("2026-10-01", 40.0, 2))

    try:
        controle.baixar_estoque("VAC002", 5)
        print("ERRO: deveria ter lancado excecao!")
    except ValueError as e:
        print("Excecao esperada capturada:", e)


def testar_descarte_vencidos():
    print("\n== Descarte de lotes vencidos (medicamentos/vacinas) ==")
    controle = ControleEstoque()
    vacina = Produto("Vacina antirrabica", "VAC001", "Fornecedor E", preco_venda=80.0)
    controle.cadastrar_produto(vacina)
    controle.adicionar_lote("VAC001", Lote("2025-01-01", 40.0, 5, data_validade="2025-06-01"))  # vencido
    controle.adicionar_lote("VAC001", Lote("2026-09-01", 42.0, 8, data_validade="2027-01-01"))  # valido

    print("Antes do descarte:", vacina.quantidade_total())
    controle.descartar_vencidos_geral(data_atual="2026-11-26")
    print("Depois do descarte:", vacina.quantidade_total())
    print("Perdas registradas:", list(vacina.perdas.percorrer()))
    assert vacina.quantidade_total() == 8


if __name__ == "__main__":
    testar_baixa_fifo()
    testar_alerta_minimo()
    testar_estoque_insuficiente()
    testar_descarte_vencidos()
    print("\nTodos os testes passaram.")
