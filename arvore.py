"""
Estrutura de dados genérica: Árvore N-ária.

ATENÇÃO (restrição do enunciado): esta árvore NÃO é binária e NÃO é uma
árvore de busca. Cada nó pode ter de 0 a N filhos. É usada para
representar a hierarquia de sistemas do animal:
    Animal -> Sistemas -> Orgaos/Estruturas -> Partes menores
"""


class NoArvore:
    """
    Nó da árvore de sistemas do animal.

    Atributos:
        nome: nome do sistema, orgao ou estrutura (ex.: "Sistema digestorio", "Estomago")
        codigo: codigo de identificacao, quando o no e um item final da
            hierarquia (None para nos que sao apenas agrupadores, como
            "Sistema digestorio")
        estado: "Saudavel" ou "Alterado"
        filhos: Lista (estrutura própria) de NoArvore
    """

    def __init__(self, nome, codigo=None, estado="Saudavel"):
        from estruturas.lista import Lista

        self.nome = nome
        self.codigo = codigo
        self.estado = estado
        self.filhos = Lista()

    def adicionar_filho(self, no_filho):
        self.filhos.inserir(no_filho)

    def eh_folha(self):
        return self.filhos.esta_vazia()


class ArvoreSistemas:
    """
    Árvore de sistemas do animal.

    Metodos:
        exibir_indentada(): imprime a árvore em pré-ordem, com indentação
        buscar_por_codigo(codigo): busca um nó pelo código
        marcar_estado(codigo, novo_estado): marca um item como
            "Saudavel" ou "Alterado" durante o diagnóstico
    """

    def __init__(self, raiz: NoArvore):
        self.raiz = raiz

    def exibir_indentada(self, no=None, nivel=0):
        """Percurso em profundidade (pré-ordem), exibindo indentado."""
        if no is None:
            no = self.raiz

        prefixo = "  " * nivel + "- "
        info = f" [{no.codigo} | {no.estado}]" if no.codigo else ""
        print(f"{prefixo}{no.nome}{info}")

        for filho in no.filhos.percorrer():
            self.exibir_indentada(filho, nivel + 1)

    def buscar_por_codigo(self, codigo, no=None):
        """Busca em profundidade um nó pelo código. Retorna o NoArvore ou None."""
        if no is None:
            no = self.raiz

        if no.codigo == codigo:
            return no

        for filho in no.filhos.percorrer():
            encontrado = self.buscar_por_codigo(codigo, filho)
            if encontrado is not None:
                return encontrado
        return None

    def marcar_estado(self, codigo, novo_estado):
        """Marca o estado (Saudavel / Alterado) de um item pelo código."""
        no = self.buscar_por_codigo(codigo)
        if no is not None:
            no.estado = novo_estado
            return True
        return False
