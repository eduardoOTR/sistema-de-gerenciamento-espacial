![Logo do Sistema](assets/logo.jpg)

---

Programa desenvolvido em Python que consulta e gerencia informações de personagens do universo Star Wars, utilizando a API [SWAPI](https://swapi.info/).

## Execução

Instale as dependências e inicie o programa:

```bash
python -m pip install -r requirements.txt
python sistema/main.py
```

Ao executar o programa (`sistema/main.py`), um menu interativo é apresentado:

1. **Buscar pessoa por nome**: Consulta o nome completo e exibe características, planeta natal, filmes, veículos e naves associados.
2. **Buscar pessoas por planeta natal**: Lista os personagens residentes no planeta informado.
3. **Buscar pessoas por prefixo do nome**: Localiza personagens cujos nomes começam com o prefixo informado.
4. **Buscar veículo por ID**: Exibe o veículo associado ao ID informado.
5. **Buscar pessoas por intervalo de massa corporal**: Lista os personagens com massa dentro dos limites informados.
6. **Transmitir informações planetárias**: Codifica os dados dos planetas com Huffman e exibe a mensagem codificada, frequências, percursos da árvore, códigos binários e taxa de compressão.
7. **Relatório de carregamento de veículos**: Calcula o maior valor de carga possível para cada veículo a partir dos pesos e valores de três caixas informados.
8. **Planejar viagem interplanetária**: Encontra o caminho de menor distância entre dois planetas utilizando Dijkstra, permite selecionar uma nave e verifica se seus consumíveis são suficientes para realizar uma viagem.
9. **Encontrar caminho que visite todos os planetas apenas uma vez e retorne ao ponto de partida**: Procura o menor ciclo hamiltoniano que visita todos os planetas cadastrados no grafo exatamente uma vez e retorna ao ponto de partida informado. Resolve o problema do caixeiro-viajante utilizando força bruta.
10. **Visualizar grafo interplanetário**: Mostra o mapa de planetas e as distâncias entre eles (com uso de Matplotlib).

0\. **Sair**: Encerra o programa.

## Estruturas e algoritmos utilizados

### Árvore Trie

Os nomes dos personagens são armazenados em uma árvore Trie (`sistema/estruturas/trie.py`). Essa estrutura permite:

- Buscar personagem por nome completo
- Pesquisar nomes por prefixo
- Realizar buscas sem diferenciar acentos, letras maiúsculas e minúsculas
- Preservar a forma original dos nomes exibidos
- Demonstrar a quantidade de nós que a estrutura percorre em cada ação

**OBS:** Cada nó da Trie possui um vetor com 256 posições para representar caracteres ASCII, evitando o uso de `dict`.

### Árvore B

A árvore B (`sistema/estruturas/b_tree.py`), com grau mínimo 3, indexa personagens pela massa corporal e permite buscar todos os registros dentro de um intervalo. Personagens com a mesma massa são armazenados juntos.

### Hashmap

O hashmap (`sistema/estruturas/hashmap.py`) associa chaves a valores usando encadeamento separado em 10 posições. É utilizado para consultar planetas, filmes, veículos e naves pelos endereços da API, além de localizar veículos e naves pelos IDs apresentados no programa.

### Grafo

O grafo ponderado (`sistema/estruturas/graph.py`) representa planetas como vértices e rotas com suas distâncias como arestas, utiliza a biblioteca NetworkX. A estrutura apresenta o algoritmo de Dijkstra para encontrar o caminho mais curto para o planejamento de viagens.

OBS: o grafo apresenta os planetas Tatooine, Dagobah, Coruscant, Alderaan, Endor, Hoth, Naboo e Mustafar.

### Codificação de Huffman

Através do algoritmo de Huffman (`sistema/estruturas/huffman.py`), foi possível:

- Contar a frequência dos caracteres
- Construir a árvore usando uma fila de prioridade
- Gerar os códigos binários
- Codificar a mensagem
- Calcular a taxa de compressão

### Mochila 0/1

O relatório de carregamento usa programação dinâmica para escolher, entre as três caixas informadas, a combinação de maior valor que respeita a capacidade de carga de cada veículo.

### Caixeiro-viajante

Testa as permutações dos planetas do grafo para encontrar o ciclo hamiltoniano de menor distância que parte e retorna ao planeta escolhido.

## Endpoints da API

O sistema consulta os seguintes endpoints da SWAPI:

- `/people/` (informações dos personagens)
- `/planets/` (informações dos planetas)
- `/films/` (informações dos filmes)
- `/vehicles/` (informações dos veículos)
- `/starships/` (informações das naves)

## Créditos

Repositório criado em conjunto por [Eduardo Ramos](https://github.com/eduardoOTR), [Felipe Ferreira](https://github.com/FelipeAndriFe) e [Rafael Bermudes](https://github.com/RafaelLBermudes).

Este projeto utiliza dados fornecidos pela [Star Wars API: SWAPI](https://swapi.info/), disponibilizados sob a [Licença MIT](https://mit-license.org/).

*Star Wars* e seus personagens, nomes e elementos associados são propriedade de seus respectivos titulares.

![Despedida](assets/hansolo.gif)
### Que a Força esteja com você!
