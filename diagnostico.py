"""
Regra de negocio: Diagnostico (Arvore de Sistemas do Animal).

O enunciado pede uma arvore PRE-DEFINIDA (nao precisa ser editavel em
estrutura, apenas usada para marcar o estado dos itens durante o
diagnostico). Usa a estrutura generica ArvoreSistemas / NoArvore
(estruturas/arvore.py), que ja garante: arvore N-aria (0 a N filhos),
nao binaria, nao de busca.

Hierarquia conforme o exemplo do enunciado:
    Animal
      Sistema digestorio
        Estomago
        Intestino
      Sistema respiratorio
        Pulmoes
        Traqueia
      Pele
        Pelos
        Unhas
"""

from estruturas.arvore import NoArvore, ArvoreSistemas


def montar_arvore_padrao():
    """
    Monta e retorna a ArvoreSistemas pre-definida do animal, com os
    codigos atribuidos as folhas (os nos agrupadores, como "Sistema
    digestorio", nao tem codigo).
    """
    animal = NoArvore("Animal")

    # --- Sistema digestorio ---
    digestorio = NoArvore("Sistema digestorio")
    digestorio.adicionar_filho(NoArvore("Estomago", codigo="DIG001"))
    digestorio.adicionar_filho(NoArvore("Intestino", codigo="DIG002"))
    animal.adicionar_filho(digestorio)

    # --- Sistema respiratorio ---
    respiratorio = NoArvore("Sistema respiratorio")
    respiratorio.adicionar_filho(NoArvore("Pulmoes", codigo="RES001"))
    respiratorio.adicionar_filho(NoArvore("Traqueia", codigo="RES002"))
    animal.adicionar_filho(respiratorio)

    # --- Pele ---
    pele = NoArvore("Pele")
    pele.adicionar_filho(NoArvore("Pelos", codigo="PEL001"))
    pele.adicionar_filho(NoArvore("Unhas", codigo="PEL002"))
    animal.adicionar_filho(pele)

    return ArvoreSistemas(animal)


class ControleDiagnostico:
    """
    Fachada para o diagnostico de um animal durante o atendimento.

    Cada animal em diagnostico recebe sua propria copia da arvore
    padrao (cada atendimento tem seu proprio estado de itens
    Saudavel / Alterado).
    """

    def __init__(self):
        self.arvore = montar_arvore_padrao()

    def exibir_diagnostico(self):
        """Exibe a arvore indentada, em pre-ordem (profundidade)."""
        self.arvore.exibir_indentada()

    def marcar_alterado(self, codigo):
        """Marca um item como 'Alterado' pelo codigo."""
        ok = self.arvore.marcar_estado(codigo, "Alterado")
        if not ok:
            raise ValueError(f"Item com codigo {codigo} nao encontrado na arvore")

    def marcar_saudavel(self, codigo):
        """Marca um item como 'Saudavel' pelo codigo."""
        ok = self.arvore.marcar_estado(codigo, "Saudavel")
        if not ok:
            raise ValueError(f"Item com codigo {codigo} nao encontrado na arvore")

    def listar_itens_alterados(self, no=None, resultado=None):
        """
        Percorre a arvore (pre-ordem) e retorna uma Lista propria com
        os nos marcados como 'Alterado'. Util para alimentar o
        prontuario.
        """
        from estruturas.lista import Lista

        if no is None:
            no = self.arvore.raiz
        if resultado is None:
            resultado = Lista()

        if no.codigo is not None and no.estado == "Alterado":
            resultado.inserir(no)

        for filho in no.filhos.percorrer():
            self.listar_itens_alterados(filho, resultado)

        return resultado


if __name__ == "__main__":
    # Teste rapido manual
    diagnostico = ControleDiagnostico()

    print("Arvore de sistemas (estado inicial):")
    diagnostico.exibir_diagnostico()

    diagnostico.marcar_alterado("RES001")  # Pulmoes
    diagnostico.marcar_alterado("PEL001")  # Pelos

    print("\nApos diagnostico do veterinario:")
    diagnostico.exibir_diagnostico()

    print("\nItens alterados encontrados:")
    for item in diagnostico.listar_itens_alterados().percorrer():
        print(" ->", item.nome, item.codigo)
