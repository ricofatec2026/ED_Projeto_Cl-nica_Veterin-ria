"""
Regra de negocio: Controle do que foi consumido / Fechamento integrado.

Integra, no momento do fechamento do prontuario:
    1. Baixa no estoque dos medicamentos/vacinas utilizados (ControleEstoque)
    2. Registro do pagamento (ControleFinanceiro)
    3. Registro de qual tutor/animal consumiu quais medicamentos
       (rastreabilidade, com base no valor do prontuario e na baixa de
       estoque)

Nao introduz uma nova estrutura de dados: orquestra as ja existentes
(Estoque, Prontuario, Pagamento), mantendo a separacao de
responsabilidades.
"""

from estruturas.lista import Lista


class RegistroConsumo:
    """
    Registro de rastreabilidade: o que um tutor/animal consumiu em um
    prontuario, com os lotes efetivamente baixados do estoque.
    """

    def __init__(self, numero_prontuario, nome_animal, nome_tutor, lotes_consumidos, valor_prontuario):
        self.numero_prontuario = numero_prontuario
        self.nome_animal = nome_animal
        self.nome_tutor = nome_tutor
        self.lotes_consumidos = lotes_consumidos  # dict: codigo_produto -> Lista de Lote
        self.valor_prontuario = valor_prontuario

    def __repr__(self):
        return (f"Consumo Prontuario#{self.numero_prontuario} - {self.nome_tutor} ({self.nome_animal}) "
                f"- Total: R$ {self.valor_prontuario:.2f}")


class ControleFechamento:
    """
    Orquestra o fechamento de um prontuario: baixa de estoque +
    pagamento + rastreabilidade do consumo.
    """

    def __init__(self, controle_estoque, controle_financeiro):
        self.controle_estoque = controle_estoque
        self.controle_financeiro = controle_financeiro
        self.registros_consumo = Lista()

    def fechar_prontuario_com_pagamento(self, prontuario, forma_pagamento, data_hora_pagamento, parcelas=1):
        """
        Fecha o prontuario (exige alta concedida), baixa do estoque
        cada medicamento utilizado (pelo lote mais antigo), registra o
        pagamento e gera o registro de rastreabilidade do consumo.
        """
        from modelos.pagamento import Pagamento

        # 1. Baixa no estoque, pelos medicamentos registrados no prontuario
        lotes_consumidos_por_produto = {}
        for item_medicamento in prontuario.medicamentos.percorrer():
            consumidos = self.controle_estoque.baixar_estoque(
                item_medicamento.codigo_produto, item_medicamento.quantidade
            )
            lotes_consumidos_por_produto[item_medicamento.codigo_produto] = consumidos

        # 2. Fecha o prontuario (valida alta concedida)
        prontuario.fechar()

        # 3. Registra o pagamento
        pagamento = Pagamento(
            nome_pagador=prontuario.nome_tutor,
            numero_prontuario=prontuario.numero,
            forma_pagamento=forma_pagamento,
            valor_medicamentos=prontuario.valor_total_medicamentos(),
            valor_procedimentos=prontuario.valor_total_procedimentos(),
            data_hora_pagamento=data_hora_pagamento,
            parcelas=parcelas,
        )
        self.controle_financeiro.registrar_pagamento(pagamento)

        # 4. Registra rastreabilidade do consumo
        registro = RegistroConsumo(
            numero_prontuario=prontuario.numero,
            nome_animal=prontuario.nome_animal,
            nome_tutor=prontuario.nome_tutor,
            lotes_consumidos=lotes_consumidos_por_produto,
            valor_prontuario=prontuario.valor_total(),
        )
        self.registros_consumo.inserir(registro)

        return pagamento, registro
