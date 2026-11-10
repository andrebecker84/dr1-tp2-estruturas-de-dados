<sub>[⬅ README](../../README.md) · [Notebook](../../andre_becker_DR1_TP2.ipynb) · [Relatório](../RELATORIO_TP2.md) · [Rubrica](rubrica-DR1-TP2.md)</sub>

# 📄 Enunciado · DR1-TP2 (Teste de Performance)

| | |
|---|---|
| **Disciplina** | Velocidade e Qualidade com Estruturas de Dados e Algoritmos |
| **Trimestre** | 26E4 |
| **Professor** | Ian Monteiro Nunes |
| **Bloco** | Ciência da Computação |
| **Turma** | GRLENGR2C2-N2-L1 |
| **Instituição** | Instituto Infnet |

> Texto do enunciado, na íntegra, como foi entregue pela disciplina. Onde cada exercício é atendido:
> [notebook](../../andre_becker_DR1_TP2.ipynb) e [relatório](../RELATORIO_TP2.md).

---

Dando continuidade ao desenvolvimento do pensamento algorítmico orientado à qualidade, este Teste de Performance 2 (TP2) aprofunda a análise de eficiência computacional, otimização de código e uso adequado de estruturas de dados fundamentais. O foco deste TP é consolidar a transição entre soluções corretas e soluções eficientes, escaláveis e justificáveis tecnicamente, ampliando o repertório de algoritmos e estruturas disponíveis.

Ao longo das atividades, você irá identificar gargalos algorítmicos, reescrever soluções ineficientes, instrumentar código para mensuração de custo computacional e empregar estruturas como hash tables, pilhas (stacks) e filas (queues). Além da implementação, será exigida análise explícita da complexidade, utilizando a notação Big O como ferramenta de comunicação técnica.

---

## Exercício 1 - Otimização de Código Quadrático com Hash Table

**Introdução**

Soluções com custo quadrático frequentemente surgem de implementações diretas baseadas em comparações repetidas. Embora funcionais, essas abordagens não escalam e se tornam inviáveis em cenários reais. Um passo essencial na formação em Ciência da Computação é aprender a identificar esses padrões e substituí-los por soluções mais eficientes, explorando estruturas de dados adequadas. Neste exercício, você irá comparar duas abordagens para o mesmo problema, evidenciando o impacto direto da escolha da estrutura de dados na eficiência algorítmica.

**Tarefa**

1. Implemente uma função que encontre o maior número único de uma lista utilizando dois laços aninhados.
2. Instrumente o código para contar o número de comparações realizadas.
3. Reescreva a função utilizando uma hash table, garantindo complexidade O(N).
4. Instrumente a versão otimizada para contabilizar acessos à estrutura.
5. Execute ambas as versões com listas de tamanhos distintos e compare os resultados.

## Exercício 2 - Interseção de Arrays em Tempo Linear

**Introdução**

Operações de interseção são recorrentes em validação de dados, sincronização de registros e cruzamento de informações. Embora uma solução baseada em laços aninhados seja simples, ela impõe um custo elevado. O uso de uma estrutura de acesso direto permite reduzir significativamente esse custo. Neste exercício, você deverá construir uma solução eficiente sem recorrer a abstrações prontas da linguagem.

**Tarefa**

1. Implemente uma função que receba dois arrays e retorne seus elementos em comum.
2. Não utilize funções prontas de interseção.
3. Utilize uma hash table para armazenar os elementos do primeiro array.
4. Garanta complexidade O(N) em relação ao total de elementos processados.
5. Valide a solução com arrays de grande tamanho.

## Exercício 3 - Detecção do Primeiro Valor Duplicado

**Introdução**

Em sistemas de processamento sequencial, a ordem dos dados pode ser tão importante quanto seu conteúdo. Identificar o primeiro valor duplicado exige uma solução que preserve a ordem de leitura e evite reprocessamentos. Este exercício reforça o uso de structures auxiliares para garantir eficiência e previsibilidade.

**Tarefa**

1. Implemente uma função que receba um array de strings e retorne o primeiro valor duplicado encontrado.
2. Considere que existe exatamente um par duplicado.
3. Utilize uma hash table para controlar os elementos já processados.
4. Garanta execução em O(N).
5. Teste com diferentes entradas.

## Exercício 4 - Letra Ausente do Alfabeto

**Introdução**

Problemas de cobertura e validação são comuns em processamento textual. Identificar elementos ausentes exige controle explícito de presença, evitando soluções redundantes. Neste exercício, você irá trabalhar com normalização de dados e marcação eficiente de ocorrências.

**Tarefa**

1. Implemente uma função que identifique a letra ausente do alfabeto em uma string.
2. Considere apenas letras de a a z.
3. Ignore maiúsculas, espaços, números e pontuação.
4. Utilize uma estrutura auxiliar para marcar presença.
5. Descreva a complexidade do algoritmo em termos de Big O.

## Exercício 5 - Primeiro Caractere Não Repetido

**Introdução**

A identificação de elementos únicos mantendo a ordem original é um problema frequente na validação e limpeza de dados. Uma solução eficiente exige separar contagem e verificação, sem múltiplas varreduras desnecessárias. Neste exercício, você irá estruturar essa lógica de forma clara e eficiente.

**Tarefa**

1. Implemente uma função que retorne o primeiro caractere não repetido de uma string.
2. Realize a contagem de frequência dos caracteres.
3. Preserve a ordem original na verificação.
4. Garanta complexidade O(N).
5. Teste com diferentes exemplos.

## Exercício 6 - Implementação e Análise do Selection Sort

**Introdução**

O Selection Sort é um algoritmo simples que permite visualizar claramente o impacto de laços aninhados no custo computacional. Embora não seja eficiente para grandes volumes, ele é uma ferramenta importante para análise e comparação de algoritmos.

**Tarefa**

1. Implemente o algoritmo Selection Sort sem utilizar funções prontas.
2. Instrumente o código para contar comparações e trocas.
3. Execute o algoritmo com listas em diferentes estados iniciais.
4. Registre os resultados obtidos.
5. Classifique a complexidade do algoritmo usando Big O.

## Exercício 7 - Implementação e Análise do Insertion Sort

**Introdução**

O Insertion Sort apresenta comportamento variável conforme o estado inicial dos dados, sendo eficiente em listas quase ordenadas. Compreender esse comportamento é essencial para avaliar algoritmos em cenários reais.

**Tarefa**

1. Implemente o algoritmo Insertion Sort em Python.
2. Instrumente o código para contar comparações e deslocamentos.
3. Teste com listas quase ordenadas e listas invertidas.
4. Compare os resultados obtidos.
5. Descreva o custo computacional no melhor e no pior caso.

## Exercício 8 - Escolha entre Pilha e Fila

**Introdução**

A escolha correta da estrutura de dados impacta diretamente o comportamento do sistema. Pilhas e filas impõem regras distintas de acesso, e a decisão entre elas deve ser técnica e justificada.

**Tarefa**

1. Analise um sistema que atende solicitações estritamente na ordem de chegada.
2. Escolha entre pilha ou fila.
3. Justifique tecnicamente sua escolha.
4. Descreva as operações envolvidas.
5. Registre a justificativa no notebook.

## Nota sobre uso de Programação Orientada a Objetos (OO)

Nos Exercícios 9 e 10, o uso de Programação Orientada a Objetos (OO) não é obrigatório, mas é fortemente recomendado.

Independentemente do paradigma adotado, o aluno precisa resolver explicitamente o problema de persistência de estado da estrutura de dados. Pilhas e filas mantêm informações internas que evoluem ao longo do tempo (array de armazenamento, índices, tamanho, capacidade), e essas informações não podem ser recriadas a cada operação.

O uso de classes facilita essa persistência ao encapsular estado e comportamento em uma única unidade, tornando o código mais claro, modular e previsível. Caso o aluno opte por uma abordagem não orientada a objetos, deverá demonstrar de forma igualmente clara e correta como o estado da pilha ou fila é mantido e atualizado entre as operações, sem perda de informação.

## Exercício 9 - Implementação de Pilha com Controle de Erros

**Introdução**

Uma implementação robusta deve tratar corretamente situações de uso indevido. Neste exercício, você irá construir uma pilha com capacidade fixa, incluindo tratamento explícito de erro.

**Tarefa**

1. Implemente uma classe Stack baseada em array.
2. Trate explicitamente overflow (inserção em pilha cheia).
3. Trate explicitamente underflow (remoção em pilha vazia).
4. Demonstre o funcionamento com uma sequência de operações.
5. Registre o estado interno após cada etapa.

## Exercício 10 - Implementação de Fila com Ponteiros

**Introdução**

Filas são fundamentais para modelar processamento sequencial. Uma implementação correta exige controle explícito de índices e tamanho.

**Tarefa**

1. Implemente uma classe Queue com capacidade fixa.
2. Utilize ponteiros para controlar início e fim.
3. Execute operações de inserção e remoção.
4. Demonstre o estado interno após cada operação.
5. Valide o comportamento FIFO.

## Exercício 11 - Reversão de String Utilizando Pilha

**Introdução**

Problemas simples podem reforçar o uso correto de estruturas de dados. A reversão de strings é um exemplo clássico de aplicação de pilhas.

**Tarefa**

1. Implemente uma função que inverta uma string utilizando uma pilha.
2. Não utilize slicing ou funções prontas de reversão.
3. Empilhe e desempilhe explicitamente os caracteres.
4. Teste com diferentes strings.
5. Apresente evidências da execução.

## Exercício 12 - Análise de Funções Hash e Distribuição

**Introdução**

A eficiência de uma hash table depende diretamente da qualidade da função hash. Funções mal distribuídas geram colisões e degradam o desempenho das operações. Neste exercício, você irá analisar criticamente diferentes funções hash simples, avaliando seu impacto na distribuição das chaves.

**Funções hash fornecidas**

Considere uma tabela hash de tamanho fixo M = 10 e as seguintes funções hash para chaves inteiras não negativas k:

* h₁(k) = k mod M
* h₂(k) = (k × 7) mod M
* h₃(k) = (k²) mod M

**Tarefa**

1. Analise as funções hash fornecidas considerando uma tabela de tamanho fixo.
2. Avalie a distribuição gerada para diferentes conjuntos de chaves.
3. Identifique as funções com maior risco de colisão.
4. Justifique suas conclusões tecnicamente.
5. Registre a análise em Markdown.

**Observações**

* Não implemente uma hash table completa.
* O foco do exercício é a qualidade da função hash e sua distribuição.
* A clareza da análise faz parte da avaliação.

---

## Entrega

Ao finalizar todos os exercícios:

1. Reúna todos os screenshots gerados durante a execução das tarefas em um único arquivo PDF.
2. Nomeie o arquivo conforme o padrão: nome_sobrenome_DR1_TP2.PDF.
3. Envie o arquivo no ambiente da disciplina.

Observação: Os screenshots devem evidenciar claramente os comandos executados e suas respectivas saídas, funcionando como complemento às evidências textuais e aos arquivos produzidos ao longo do TP.

Consulte o material de apoio em https://fabiolinhares.com.br/infnet/estruturas-dados-algoritmos-tp1.html e a bibliografia recomendada: A Common-Sense Guide to Data Structures and Algorithms in Python, Volume 1, de Jay Wengrow (Editora Pragmatic Bookshelf / O'Reilly Learning: https://learning.oreilly.com/library/view/a-common-sense-guide/9798888650776/f_0004.xhtml).
