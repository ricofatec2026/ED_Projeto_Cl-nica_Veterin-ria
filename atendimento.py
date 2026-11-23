"""
Regra de negocio: Controle de Atendimento (fila de espera dos animais).

Combinacao de estruturas (documentar no README):
    Fila (emergencia) + Fila (normal)
    -> o proximo animal chamado vem da fila de emergencia, se nao
       estiver vazia; senao, vem da fila normal.
"""

from estruturas.fila import Fila


class AnimalEspera:
    """Representa um animal aguardando atendimento."""

    def __init__(self, nome_animal, nome_tutor, data_hora_chegada, queixa, emergencia=False):
        self.nome_animal = nome_animal
        self.nome_tutor = nome_tutor
        self.data_hora_chegada = data_hora_chegada
        self.queixa = queixa
        self.emergencia = emergencia

    def __repr__(self):
        tag = "[EMERGENCIA] " if self.emergencia else ""
        return f"{tag}{self.nome_animal} ({self.nome_tutor}) - {self.queixa}"


class ControleAtendimento:
    """
    Gerencia a fila de espera de animais, com prioridade para emergencia.

    Duas filas proprias trabalhando juntas (combinacao de estruturas):
    - fila_emergencia: animais trazidos em caso de emergencia
    - fila_normal: demais animais
    """

    def __init__(self):
        self.fila_emergencia = Fila()
        self.fila_normal = Fila()

    def chegar_animal(self, animal: AnimalEspera):
        """Adiciona um animal na fila correta, conforme emergencia ou nao."""
        if animal.emergencia:
            self.fila_emergencia.enfileirar(animal)
        else:
            self.fila_normal.enfileirar(animal)

    def proximo_animal(self):
        """
        Quando um consultorio fica livre: retorna o proximo animal a
        ser atendido. Prioridade para a fila de emergencia; se vazia,
        usa a fila normal.
        """
        if not self.fila_emergencia.esta_vazia():
            return self.fila_emergencia.desenfileirar()
        return self.fila_normal.desenfileirar()

    def esta_vazia(self):
        return self.fila_emergencia.esta_vazia() and self.fila_normal.esta_vazia()


if __name__ == "__main__":
    # Teste rapido manual
    controle = ControleAtendimento()
    controle.chegar_animal(AnimalEspera("Rex", "Joao", "26/11 08:00", "Vomito"))
    controle.chegar_animal(AnimalEspera("Mel", "Maria", "26/11 08:05", "Atropelamento", emergencia=True))
    controle.chegar_animal(AnimalEspera("Tom", "Pedro", "26/11 08:10", "Falta de apetite"))

    print("Chamando animais na ordem correta (emergencia primeiro):")
    while not controle.esta_vazia():
        print(" ->", controle.proximo_animal())
