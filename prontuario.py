"""
Regra de negocio: Prontuario de Atendimento.

Cada animal atendido recebe um prontuario, que acumula medicamentos e
procedimentos ao longo do diagnostico/atendimento. O prontuario so pode
ser fechado depois que o animal receber alta (flag 'alta_concedida').

Medicamentos e procedimentos usados no prontuario: Lista propria
(quantidade variavel, adicionados/removidos ao longo do atendimento).
"""

from estruturas.lista import Lista


class ItemMedicamento:
    """Medicamento/vacina aplicado no prontuario (associado a um produto do estoque)."""

    def __init__(self, codigo_produto, nome, quantidade, preco_unitario):
        self.codigo_produto = codigo_produto
        self.nome = nome
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

    def valor_total(self):
        return self.quantidade * self.preco_unitario

    def __repr__(self):
        return f"{self.nome} x{self.quantidade} (R$ {self.valor_total():.2f})"


class ItemProcedimento:
    """Procedimento realizado no prontuario (ex.: consulta, vacina, curativo, exame)."""

    def __init__(self, descricao, valor):
        self.descricao = descricao
        self.valor = valor

    def __repr__(self):
        return f"{self.descricao} (R$ {self.valor:.2f})"


class Prontuario:
    """
    Representa um Prontuario de Atendimento aberto para um animal.

    Estado:
        aberto -> em andamento, medicamentos/procedimentos podem ser
                  adicionados ou removidos, alta ainda nao concedida
        fechado -> alta concedida e prontuario fechado (ponto de corte
                   para pagamento)
    """

    _proximo_numero = 1  # contador simples para gerar numero de prontuario

    def __init__(self, nome_animal, nome_tutor, veterinario_responsavel, data_hora_abertura):
        self.numero = Prontuario._proximo_numero
        Prontuario._proximo_numero += 1

        self.nome_animal = nome_animal
        self.nome_tutor = nome_tutor
        self.veterinario_responsavel = veterinario_responsavel
        self.data_hora_abertura = data_hora_abertura

        self.medicamentos = Lista()
        self.procedimentos = Lista()

        self.alta_concedida = False
        self.fechado = False

    # --- Medicamentos ---

    def adicionar_medicamento(self, item: ItemMedicamento):
        if self.fechado:
            raise ValueError(f"Prontuario #{self.numero} ja esta fechado, nao e possivel adicionar medicamentos")
        self.medicamentos.inserir(item)

    def remover_medicamento(self, codigo_produto):
        """Remove um medicamento do prontuario (ex.: tutor nao autorizou)."""
        if self.fechado:
            raise ValueError(f"Prontuario #{self.numero} ja esta fechado, nao e possivel remover medicamentos")
        return self.medicamentos.remover(lambda m: m.codigo_produto == codigo_produto)

    # --- Procedimentos ---

    def adicionar_procedimento(self, item: ItemProcedimento):
        if self.fechado:
            raise ValueError(f"Prontuario #{self.numero} ja esta fechado, nao e possivel adicionar procedimentos")
        self.procedimentos.inserir(item)

    def remover_procedimento(self, descricao):
        if self.fechado:
            raise ValueError(f"Prontuario #{self.numero} ja esta fechado, nao e possivel remover procedimentos")
        return self.procedimentos.remover(lambda p: p.descricao == descricao)

    # --- Totais ---

    def valor_total_medicamentos(self):
        total = 0.0
        for medicamento in self.medicamentos.percorrer():
            total += medicamento.valor_total()
        return total

    def valor_total_procedimentos(self):
        total = 0.0
        for procedimento in self.procedimentos.percorrer():
            total += procedimento.valor
        return total

    def valor_total(self):
        return self.valor_total_medicamentos() + self.valor_total_procedimentos()

    # --- Ciclo de vida ---

    def conceder_alta(self):
        self.alta_concedida = True

    def fechar(self):
        """So pode fechar depois que a alta tiver sido concedida."""
        if not self.alta_concedida:
            raise ValueError(
                f"Prontuario #{self.numero} nao pode ser fechado: alta ainda nao concedida"
            )
        self.fechado = True

    def __repr__(self):
        status = "FECHADO" if self.fechado else "ABERTO"
        return (f"Prontuario #{self.numero} [{status}] - {self.nome_animal} "
                f"- {self.nome_tutor} - Total: R$ {self.valor_total():.2f}")


class ControleProntuarios:
    """
    Gerencia a Lista de prontuarios abertos/fechados na clinica.
    """

    def __init__(self):
        self.prontuarios = Lista()

    def abrir_prontuario(self, nome_animal, nome_tutor, veterinario_responsavel, data_hora_abertura):
        prontuario_novo = Prontuario(nome_animal, nome_tutor, veterinario_responsavel, data_hora_abertura)
        self.prontuarios.inserir(prontuario_novo)
        return prontuario_novo

    def buscar_por_numero(self, numero):
        return self.prontuarios.buscar(lambda p: p.numero == numero)

    def buscar_por_animal(self, nome_animal):
        """Retorna o prontuario aberto mais recente para o animal (busca simples)."""
        encontrado = None
        for prontuario_atual in self.prontuarios.percorrer():
            if prontuario_atual.nome_animal == nome_animal and not prontuario_atual.fechado:
                encontrado = prontuario_atual
        return encontrado


if __name__ == "__main__":
    # Teste rapido manual
    controle = ControleProntuarios()

    prontuario1 = controle.abrir_prontuario("Rex", "Joao Silva", "Dra. Ana", "26/11 09:00")
    prontuario1.adicionar_medicamento(ItemMedicamento("VAC001", "Vacina antirrabica", 1, 80.0))
    prontuario1.adicionar_procedimento(ItemProcedimento("Consulta", 100.0))
    prontuario1.adicionar_procedimento(ItemProcedimento("Exame de sangue", 60.0))

    print(prontuario1)
    print("Medicamentos:", list(prontuario1.medicamentos.percorrer()))
    print("Procedimentos:", list(prontuario1.procedimentos.percorrer()))

    # tutor nao autorizou o exame
    prontuario1.remover_procedimento("Exame de sangue")
    print("\nApos remover exame de sangue:")
    print(prontuario1)

    try:
        prontuario1.fechar()
        print("ERRO: deveria ter lancado excecao (alta nao concedida)!")
    except ValueError as e:
        print("\nExcecao esperada capturada:", e)

    prontuario1.conceder_alta()
    prontuario1.fechar()
    print("\nApos conceder alta e fechar:")
    print(prontuario1)
