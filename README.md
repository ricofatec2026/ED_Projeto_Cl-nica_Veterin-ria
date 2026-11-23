# Clínica Veterinária — Projeto de Estrutura de Dados

Sistema de gestão de uma clínica veterinária: tutores/animais, fila de
atendimento, diagnóstico (árvore de sistemas do animal), estoque de
medicamentos/vacinas por lote, prontuários de atendimento e pagamento.

Disciplina: Estrutura de Dados — Fatec Rio Claro
Linguagem: Python puro (sem bibliotecas built-in para as estruturas de
dados do problema; estruturas implementadas do zero).

## Estrutura do repositório

```
clinica_veterinaria/
├── estruturas/        # Estruturas de dados genéricas (sem regra de negócio)
│   ├── lista.py         # Lista encadeada própria
│   ├── fila.py           # Fila (FIFO) própria
│   ├── pilha.py          # Pilha (LIFO) própria
│   └── arvore.py         # Árvore N-ária própria
├── modelos/            # Regras de negócio da clínica (usam as estruturas acima)
│   ├── atendimento.py    # Controle de atendimento (fila emergência + fila normal)
│   └── tutor.py          # Controle de tutores e animais (lista + lista)
├── testes/
│   ├── teste_estruturas.py
│   └── teste_tutores.py
└── README.md
```

## Status atual (em desenvolvimento)

- [x] Estruturas genéricas: Lista, Fila, Pilha, Árvore N-ária
- [x] Controle de Atendimento (fila emergência + fila normal)
- [x] Controle de Tutores e Animais (Lista de tutores, cada um com Lista de animais)
- [ ] Árvore de Sistemas do Animal pré-definida (diagnóstico)
- [ ] Controle de Estoque (Lista de produtos, cada um com Fila de lotes)
- [ ] Prontuário de Atendimento
- [ ] Controle de Pagamento
- [ ] Menu interativo (em vez de simulação fixa) + vídeo da apresentação

## Combinações de estruturas (obrigatório pelo enunciado)

### 1. Atendimento com prioridade para emergência — Fila + Fila
**Classes envolvidas:** `ControleAtendimento` (modelos/atendimento.py),
usando duas instâncias de `Fila` (estruturas/fila.py): `fila_emergencia`
e `fila_normal`.
**Método:** `ControleAtendimento.proximo_animal()` — consome primeiro
da `fila_emergencia`; se vazia, consome da `fila_normal`.
**Justificativa:** separar em duas filas garante O(1) para decidir o
próximo animal, mantendo a ordem de chegada dentro de cada categoria.
Usar uma única fila exigiria reordenar ou varrer a fila inteira toda
vez que um caso de emergência chegasse, o que é O(n) e quebra a ordem
de chegada dos demais animais.

### 2. Estoque com vários lotes por medicamento — Lista + Fila
*(a implementar)* Lista de produtos, cada produto contendo uma Fila de
lotes. A baixa de estoque percorre a lista até achar o produto e
consome a fila do lote mais antigo (FIFO).

### 3. Tutores e seus animais — Lista + Lista
**Classes envolvidas:** `ControleTutores` (modelos/tutor.py), que
mantém uma `Lista` (estruturas/lista.py) de `Tutor`; cada `Tutor`
mantém sua própria `Lista` de `Animal`.
**Método:** `ControleTutores.buscar_animal_por_nome_e_cpf(cpf, nome)` —
localiza o tutor pelo CPF e depois busca o animal pelo nome na lista
desse tutor.
**Justificativa:** cada tutor é dono natural de seus animais, então
aninhar uma lista dentro da outra reflete o domínio do problema e
permite que cada tutor cadastre novos animais ao longo do tempo, sem
limite pré-definido. Uma única lista global de animais exigiria uma
referência extra ao tutor em cada animal e perderia a relação direta
de posse; remover um tutor também não removeria automaticamente seus
animais.

## Cronograma de desenvolvimento (commits diários)

| Dia | Entrega |
|---|---|
| 1 (hoje) | Estruturas genéricas (Lista, Fila, Pilha, Árvore) + Controle de Atendimento + Tutores/Animais |
| 2 | Árvore de Sistemas do Animal + Controle de Estoque + Prontuário de Atendimento |
| 3 | Controle de Pagamento + fechamento integrado + menu interativo + gravação do vídeo |

**Prazo final:** início da aula do dia 26/11/2026 (link do repositório + link do vídeo).

## Observações sobre a implementação

- Nenhuma estrutura built-in do Python (`list`, `dict`, `queue.Queue`,
  etc.) é usada para resolver as estruturas de dados do problema. Elas
  são implementadas do zero com nós encadeados próprios.
- Separação de responsabilidades: `estruturas/` contém apenas
  estruturas de dados puras e reutilizáveis; `modelos/` contém as
  regras específicas da clínica, que usam as estruturas de `estruturas/`.
- Diferente do projeto anterior (Oficina Mecânica), este projeto terá
  um **menu interativo** no lugar de uma simulação fixa, permitindo
  inserir dados manualmente durante a execução.
