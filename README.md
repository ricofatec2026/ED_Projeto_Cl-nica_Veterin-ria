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
├── estruturas/           # Estruturas de dados genéricas (sem regra de negócio)
│   ├── lista.py            # Lista encadeada própria
│   ├── fila.py             # Fila (FIFO) própria
│   ├── pilha.py            # Pilha (LIFO) própria
│   └── arvore.py           # Árvore N-ária própria
├── modelos/               # Regras de negócio da clínica (usam as estruturas acima)
│   ├── atendimento.py       # Controle de atendimento (fila emergência + fila normal)
│   ├── tutor.py             # Controle de tutores e animais (lista + lista)
│   ├── diagnostico.py       # Diagnóstico via árvore de sistemas pré-definida
│   ├── estoque.py           # Controle de estoque (lista de produtos + fila de lotes)
│   ├── prontuario.py        # Prontuário de Atendimento (medicamentos, procedimentos, fechamento)
│   ├── pagamento.py         # Controle de Pagamento
│   └── fechamento.py        # Integra prontuário + estoque + pagamento + rastreabilidade
├── testes/
│   ├── teste_estruturas.py
│   ├── teste_tutores.py
│   ├── teste_diagnostico.py
│   ├── teste_estoque.py
│   ├── teste_prontuario.py
│   └── teste_pagamento.py
├── main.py                # Menu interativo (entrada manual de dados)
└── README.md
```

## Status atual — projeto concluído

- [x] Estruturas genéricas: Lista, Fila, Pilha, Árvore N-ária
- [x] Controle de Atendimento (fila emergência + fila normal)
- [x] Controle de Tutores e Animais (Lista de tutores, cada um com Lista de animais)
- [x] Árvore de Sistemas do Animal pré-definida (diagnóstico)
- [x] Controle de Estoque (Lista de produtos, cada um com Fila de lotes)
- [x] Prontuário de Atendimento
- [x] Controle de Pagamento
- [x] Menu interativo (entrada manual, cobrindo o fluxo completo)

**Rodar o sistema:** `python main.py` (a partir da raiz do projeto).

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
**Classes envolvidas:** `ControleEstoque` (modelos/estoque.py), que
mantém uma `Lista` de `Produto`; cada `Produto` mantém sua própria
`Fila` de `Lote`.
**Método:** `ControleEstoque.baixar_estoque(codigo, quantidade)` →
`Produto.baixar_estoque(...)` — percorre a lista até achar o produto e
consome a fila de lotes a partir da frente (lote mais antigo), passando
para o próximo lote quando o atual não é suficiente.
**Justificativa:** a Fila garante FIFO nativamente, sem precisar
ordenar os lotes por data a cada baixa — o lote mais antigo já está
sempre na frente. Usar uma única lista de lotes misturada exigiria
ordenação a cada operação ou controle manual de "qual é o mais antigo",
o que é mais custoso e propenso a erro.

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

## Menu interativo (main.py)

Diferente do projeto anterior (Oficina Mecânica, que usava uma
simulação fixa), este projeto usa um **menu interativo**, permitindo
inserir os dados manualmente durante a execução. O menu cobre o fluxo
completo pedido no enunciado:

1. **Cadastro de tutores e animais** (opções 1–4)
2. **Chegada do animal e entrada na espera** (opção 5) — normal ou
   emergência
3. **Chamada do próximo animal e abertura do prontuário** (opção 6)
4. **Diagnóstico na árvore de sistemas** (opção 7) — marca itens como
   "Alterado"
5. **Cadastro de produtos e lotes no estoque** (opções 8–10)
6. **Inclusão de medicamentos e procedimentos no prontuário** (opções
   11–13)
7. **Alta, fechamento do prontuário e pagamento** (opção 14) — orquestra,
   nesta ordem: baixa de estoque pelo lote mais antigo, fechamento do
   prontuário (valida alta concedida), registro do pagamento e registro
   de rastreabilidade do consumo
8. **Faturamento total** (opção 15)

`ControleFechamento` (modelos/fechamento.py) não cria uma nova
estrutura de dados — ele integra as já existentes (Estoque, Prontuário,
Pagamento), mantendo a separação de responsabilidades: cada módulo
cuida da sua parte, e o fechamento cuida apenas da orquestração entre
eles.

## Observações sobre a implementação

- Nenhuma estrutura built-in do Python (`list`, `dict`, `queue.Queue`,
  etc.) é usada para resolver as estruturas de dados do problema. Elas
  são implementadas do zero com nós encadeados próprios, em
  `estruturas/`.
- Separação de responsabilidades: `estruturas/` contém apenas
  estruturas de dados puras e reutilizáveis; `modelos/` contém as
  regras específicas da clínica, que usam as estruturas de
  `estruturas/`; `main.py` cuida apenas da interação com o usuário
  (entrada/saída de dados), delegando toda a lógica aos módulos.
- Todos os módulos têm testes manuais em `testes/`, cobrindo o caminho
  feliz e casos de borda (dados duplicados, estoque insuficiente,
  fechamento antes da alta concedida, forma de pagamento inválida,
  etc.).
- O menu interativo foi testado de ponta a ponta com um fluxo completo
  de entrada simulada, cobrindo cadastro, atendimento, diagnóstico,
  estoque, prontuário e fechamento com pagamento.
