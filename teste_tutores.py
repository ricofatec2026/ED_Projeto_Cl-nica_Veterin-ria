"""
Testes manuais do Controle de Tutores e Animais.
Rodar com: python -m testes.teste_tutores (a partir da raiz do projeto)
"""

from modelos.tutor import ControleTutores, Tutor, Animal


def testar_cadastro_e_busca():
    print("== Cadastro e busca ==")
    controle = ControleTutores()

    controle.cadastrar_tutor(Tutor("Joao Silva", "111.111.111-11", "19999990000"))
    controle.cadastrar_animal("111.111.111-11", Animal("Rex", "Cachorro", "Labrador", 3))
    controle.cadastrar_animal("111.111.111-11", Animal("Mia", "Gato", "Siames", 2))

    controle.cadastrar_tutor(Tutor("Maria Souza", "222.222.222-22", "19988887777"))
    controle.cadastrar_animal("222.222.222-22", Animal("Tom", "Cachorro", "Vira-lata", 5))

    tutor = controle.buscar_tutor_por_cpf("222.222.222-22")
    print("Tutor encontrado:", tutor)

    dono, animal = controle.buscar_animal_por_nome_e_cpf("111.111.111-11", "Mia")
    print("Animal Mia pertence a:", dono.nome, "->", animal)


def testar_remocao():
    print("\n== Remocao ==")
    controle = ControleTutores()
    controle.cadastrar_tutor(Tutor("Pedro Costa", "333.333.333-33", "19977776666"))
    controle.cadastrar_animal("333.333.333-33", Animal("Bidu", "Cachorro", "Poodle", 4))

    removido = controle.remover_animal("333.333.333-33", "Bidu")
    print("Animal removido:", removido)

    _, animal = controle.buscar_animal_por_nome_e_cpf("333.333.333-33", "Bidu")
    print("Apos remover, busca retorna:", animal)

    tutor_removido = controle.remover_tutor("333.333.333-33")
    print("Tutor removido:", tutor_removido)
    print("Busca apos remover tutor:", controle.buscar_tutor_por_cpf("333.333.333-33"))


def testar_cpf_duplicado():
    print("\n== CPF duplicado (deve lancar erro) ==")
    controle = ControleTutores()
    controle.cadastrar_tutor(Tutor("Ana", "444.444.444-44", "19955554444"))
    try:
        controle.cadastrar_tutor(Tutor("Ana Duplicada", "444.444.444-44", "19900001111"))
        print("ERRO: deveria ter lancado excecao!")
    except ValueError as e:
        print("Excecao esperada capturada:", e)


if __name__ == "__main__":
    testar_cadastro_e_busca()
    testar_remocao()
    testar_cpf_duplicado()
