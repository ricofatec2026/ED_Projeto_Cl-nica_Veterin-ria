"""
Regra de negocio: Controle de Tutores e Animais.

Combinacao de estruturas (documentar no README):
    Lista (tutores) + Lista (animais de cada tutor)
    -> cada Tutor guarda uma Lista propria de Animal.
       Buscar um animal (pelo nome + CPF do tutor) percorre a lista de
       tutores e, para cada um, a lista de animais.
"""

from estruturas.lista import Lista


class Animal:
    """Representa um animal cadastrado na clinica."""

    def __init__(self, nome, especie, raca, idade):
        self.nome = nome
        self.especie = especie
        self.raca = raca
        self.idade = idade

    def __repr__(self):
        return f"{self.nome} - {self.especie}/{self.raca} ({self.idade} anos)"


class Tutor:
    """
    Representa um tutor da clinica.

    Cada tutor possui sua propria Lista de animais, que pode crescer
    sem limite pre-definido ao longo do tempo.
    """

    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.animais = Lista()

    def adicionar_animal(self, animal: Animal):
        self.animais.inserir(animal)

    def remover_animal(self, nome_animal):
        """Remove um animal deste tutor pelo nome. Retorna o animal removido ou None."""
        return self.animais.remover(lambda a: a.nome == nome_animal)

    def buscar_animal(self, nome_animal):
        """Busca um animal deste tutor pelo nome."""
        return self.animais.buscar(lambda a: a.nome == nome_animal)

    def __repr__(self):
        return f"{self.nome} (CPF: {self.cpf}) - {len(self.animais)} animal(is)"


class ControleTutores:
    """
    Gerencia a Lista de tutores da clinica.

    Metodos:
        cadastrar_tutor(tutor)
        buscar_tutor_por_cpf(cpf)
        remover_tutor(cpf)
        cadastrar_animal(cpf, animal)
        buscar_animal_por_nome_e_cpf(cpf, nome_animal) -> busca direta no tutor
        remover_animal(cpf, nome_animal)
    """

    def __init__(self):
        self.tutores = Lista()

    # --- Tutores ---

    def cadastrar_tutor(self, tutor: Tutor):
        if self.buscar_tutor_por_cpf(tutor.cpf) is not None:
            raise ValueError(f"Ja existe tutor cadastrado com CPF {tutor.cpf}")
        self.tutores.inserir(tutor)

    def buscar_tutor_por_cpf(self, cpf):
        return self.tutores.buscar(lambda t: t.cpf == cpf)

    def remover_tutor(self, cpf):
        """Remove um tutor (e, com ele, seus animais) pelo CPF."""
        return self.tutores.remover(lambda t: t.cpf == cpf)

    # --- Animais (combinacao Lista + Lista) ---

    def cadastrar_animal(self, cpf, animal: Animal):
        """Adiciona um animal a um tutor ja cadastrado, buscando-o pelo CPF."""
        tutor = self.buscar_tutor_por_cpf(cpf)
        if tutor is None:
            raise ValueError(f"Tutor com CPF {cpf} nao encontrado")
        tutor.adicionar_animal(animal)

    def buscar_animal_por_nome_e_cpf(self, cpf, nome_animal):
        """
        Busca pelo nome do animal junto com o CPF do tutor (conforme
        exigido no enunciado: busca por nome do animal + CPF).
        Percorre a lista de tutores ate achar o CPF, depois a lista de
        animais desse tutor ate achar o nome.
        """
        tutor = self.buscar_tutor_por_cpf(cpf)
        if tutor is None:
            return None, None
        animal = tutor.buscar_animal(nome_animal)
        return tutor, animal

    def remover_animal(self, cpf, nome_animal):
        """Remove um animal de um tutor especifico, pelo CPF + nome do animal."""
        tutor = self.buscar_tutor_por_cpf(cpf)
        if tutor is None:
            return None
        return tutor.remover_animal(nome_animal)


if __name__ == "__main__":
    # Teste rapido manual
    controle = ControleTutores()

    joao = Tutor("Joao Silva", "111.111.111-11", "19999990000")
    controle.cadastrar_tutor(joao)
    controle.cadastrar_animal("111.111.111-11", Animal("Rex", "Cachorro", "Labrador", 3))
    controle.cadastrar_animal("111.111.111-11", Animal("Mia", "Gato", "Siames", 2))

    maria = Tutor("Maria Souza", "222.222.222-22", "19988887777")
    controle.cadastrar_tutor(maria)
    controle.cadastrar_animal("222.222.222-22", Animal("Tom", "Cachorro", "Vira-lata", 5))

    print("Busca por CPF:", controle.buscar_tutor_por_cpf("111.111.111-11"))

    tutor, animal = controle.buscar_animal_por_nome_e_cpf("111.111.111-11", "Mia")
    print("Busca por nome+CPF:", animal, "| tutor:", tutor.nome)

    removido = controle.remover_animal("111.111.111-11", "Rex")
    print("Animal removido:", removido)
    print("Animais restantes de Joao:", list(joao.animais.percorrer()))
