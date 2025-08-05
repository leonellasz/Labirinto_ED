# Solucionador de Labirinto - Backtracking Visual

Um programa em Python que resolve labirintos usando o algoritmo de **backtracking** com visualização em tempo real usando Pygame.

## Descrição

Este projeto implementa a solução clássica do problema do labirinto, onde um jogador precisa sair de uma posição inicial e encontrar o tesouro contido no labirinto. O algoritmo utiliza uma estrutura de pilha para implementar o backtracking de forma eficiente.

## Algoritmo Backtracking

O algoritmo segue os seguintes passos:

1. **Criar uma nova pilha**
2. **Localizar a posição inicial do jogador**
3. **Inserir sua localização na pilha**
4. **Enquanto a pilha não estiver vazia:**
   - Retirar uma localização (linha, coluna) da pilha
   - Se a posição tiver o prêmio no local, então o caminho foi encontrado
   - Caso contrário, se este local não contiver o prêmio:
     - Mover o jogador para este local
     - Examinar se as casas adjacentes estão livres
     - Se sim, inserir sua posição na pilha
5. **Retornar resultado**

## Requisitos

- Python 3.6 ou superior
- Pygame

### Instalação do Pygame

```bash
pip install pygame
```

## Como Usar

1. **Execute o programa:**
   ```bash
   python maze_solver.py
   ```

2. **Escolha o tipo de labirinto:**
   - 1 - Pequeno (8x8)
   - 2 - Médio (12x12)
   - 3 - Aleatório (15x15)

3. **Use os controles para interagir:**
   - **SPACE** - Iniciar resolução
   - **R** - Reset do labirinto
   - **↑/↓** - Ajustar velocidade de resolução
   - **ESC** - Sair do programa

## Representação do Labirinto

O labirinto é representado por uma matriz 2D onde:

- **0** = Parede (cor preta)
- **1** = Caminho livre (cor branca)
- **2** = Posição inicial (cor amarela)
- **3** = Tesouro/Objetivo (cor laranja)

## Cores da Visualização

Durante a execução, as cores indicam:

- **Preto** - Paredes do labirinto
- **Amarelo** - Posição inicial do jogador
- **Laranja** - Localização do tesouro
- **Vermelho** - Posição atual sendo explorada
- **Cinza** - Células já visitadas durante a busca
- **Verde** - Caminho da solução final

## Estrutura do Código

### Classe Principal: `MazeSolverSimple`

**Métodos principais:**

- `find_positions()` - Localiza início e tesouro no labirinto
- `get_adjacent_positions()` - Retorna posições adjacentes válidas
- `solve_step()` - Executa um passo do algoritmo backtracking
- `reconstruct_path()` - Reconstrói o caminho da solução
- `draw_maze()` - Renderiza o labirinto na tela
- `handle_events()` - Gerencia entrada do usuário
- `run()` - Loop principal da aplicação

### Estruturas de Dados Utilizadas

- **Pilha (stack)** - Para implementar o backtracking
- **Conjunto (visited)** - Para rastrear células visitadas
- **Dicionário (parent)** - Para reconstruir o caminho da solução
- **Lista (solution_path)** - Para armazenar o caminho final

## Funcionamento do Algoritmo

1. **Inicialização**: A pilha é inicializada com a posição de início
2. **Exploração**: O algoritmo remove uma posição da pilha e a marca como visitada
3. **Verificação**: Se a posição atual é o tesouro, a solução foi encontrada
4. **Expansão**: Adiciona todas as posições adjacentes válidas à pilha
5. **Backtracking**: Quando não há mais movimentos válidos, o algoritmo retrocede
6. **Solução**: O caminho é reconstruído usando o rastreamento de pais

## Características do Backtracking

- **Exploração sistemática** de todos os caminhos possíveis
- **Retrocesso automático** quando encontra becos sem saída
- **Garantia de encontrar solução** se ela existir
- **Otimização de memória** através da pilha
- **Reconstituição do caminho** apenas da solução final

## Exemplos de Labirintos

### Labirinto Pequeno (8x8)
```
0 0 0 0 0 0 0 0
0 2 1 1 0 1 1 0
0 0 0 1 0 1 0 0
0 1 1 1 1 1 1 0
0 1 0 0 0 0 1 0
0 1 1 1 1 1 1 0
0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0
```

### Legenda
- `2` = Início (amarelo)
- `3` = Tesouro (laranja)
- `1` = Caminho livre
- `0` = Parede

## Personalização

Você pode facilmente criar seus próprios labirintos modificando as matrizes no código ou implementando um gerador de labirintos personalizado.

### Exemplo de Labirinto Customizado

```python
meu_labirinto = [
    [0, 0, 0, 0, 0],
    [0, 2, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 3, 0, 0, 0]
]
```

## Solução de Problemas

### Erro: "Pygame não encontrado"
```bash
pip install pygame
```

### Erro: "Sem solução encontrada"
- Verifique se existe um caminho válido entre início (2) e tesouro (3)
- Certifique-se de que ambos estão presentes no labirinto

### Performance lenta
- Use labirintos menores
- Aumente a velocidade com as teclas ↑/↓

## Contribuições

Sinta-se livre para contribuir com melhorias:

- Novos algoritmos de resolução (A*, Dijkstra)
- Gerador de labirintos mais sofisticado
- Interface de usuário aprimorada
- Estatísticas de performance
- Modo de comparação entre algoritmos

## Conceitos Aprendidos

Este projeto demonstra:

- **Algoritmos de backtracking**
- **Estruturas de dados (pilha, conjunto, dicionário)**
- **Programação orientada a objetos**
- **Visualização com Pygame**
- **Algoritmos de busca em grafos**
- **Reconstrução de caminhos**
