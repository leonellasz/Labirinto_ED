import pygame
import sys
import time
from collections import deque
import random


class MazeSolverSimple:
    def __init__(self, maze, cell_size=30):
        """
        Inicializa o solucionador visual simples de labirinto.

        Args:
            maze: Lista 2D representando o labirinto
            cell_size: Tamanho de cada célula em pixels
        """
        self.maze = [row[:] for row in maze]
        self.original_maze = [row[:] for row in maze]
        self.rows = len(maze)
        self.cols = len(maze[0]) if maze else 0
        self.cell_size = cell_size

        # Estruturas do algoritmo
        self.stack = []
        self.visited = set()
        self.solution_path = []
        self.parent = {}
        self.current_pos = None

        # Cores simples
        self.colors = {
            'wall': (0, 0, 0),  # Preto - parede
            'path': (255, 255, 255),  # Branco - caminho livre
            'start': (255, 255, 0),  # Amarelo - início
            'treasure': (255, 165, 0),  # Laranja - tesouro
            'visited': (200, 200, 200),  # Cinza - visitado
            'current': (255, 0, 0),  # Vermelho - posição atual
            'solution': (0, 255, 0),  # Verde - solução
            'background': (128, 128, 128)  # Cinza de fundo
        }

        # Inicializar Pygame
        pygame.init()
        self.font = pygame.font.Font(None, 36)

        # Configurar janela - apenas o labirinto
        self.window_width = self.cols * self.cell_size
        self.window_height = self.rows * self.cell_size + 60  # +60 para título

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Solucionador de Labirinto - Backtracking")

        # Estado da simulação
        self.solving = False
        self.solved = False
        self.speed = 100  # millisegundos entre passos

    def find_positions(self):
        """Encontra as posições inicial e do tesouro."""
        start = None
        treasure = None

        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == 2:
                    start = (i, j)
                elif self.maze[i][j] == 3:
                    treasure = (i, j)

        return start, treasure

    def get_adjacent_positions(self, row, col):
        """Retorna posições adjacentes válidas."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        adjacent = []

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if (0 <= new_row < self.rows and
                    0 <= new_col < self.cols and
                    self.maze[new_row][new_col] != 0 and
                    (new_row, new_col) not in self.visited):
                adjacent.append((new_row, new_col))

        return adjacent

    def reconstruct_path(self, end_pos):
        """Reconstrói o caminho da solução."""
        path = []
        current = end_pos

        while current is not None:
            path.append(current)
            current = self.parent.get(current)

        return path[::-1]

    def draw_maze(self):
        """Desenha o labirinto."""
        # Desenhar células
        for i in range(self.rows):
            for j in range(self.cols):
                pos = (i, j)
                x = j * self.cell_size
                y = i * self.cell_size + 50  # +50 para espaço do título

                # Determinar cor
                if self.maze[i][j] == 0:  # Parede
                    color = self.colors['wall']
                elif self.maze[i][j] == 2:  # Início
                    color = self.colors['start']
                elif self.maze[i][j] == 3:  # Tesouro
                    color = self.colors['treasure']
                elif pos == self.current_pos:  # Posição atual
                    color = self.colors['current']
                elif pos in self.solution_path and self.solved:  # Solução
                    color = self.colors['solution']
                elif pos in self.visited:  # Visitado
                    color = self.colors['visited']
                else:  # Caminho livre
                    color = self.colors['path']

                # Desenhar célula
                pygame.draw.rect(self.screen, color,
                                 (x, y, self.cell_size, self.cell_size))

                # Desenhar borda
                pygame.draw.rect(self.screen, (100, 100, 100),
                                 (x, y, self.cell_size, self.cell_size), 1)

    def draw_title(self):
        """Desenha o título simples."""
        if self.solved:
            title = "LABIRINTO SOLUCIONADO!"
            color = self.colors['solution']
        elif self.solving:
            title = "RESOLVENDO..."
            color = self.colors['current']
        else:
            title = "Pressione SPACE para resolver"
            color = (255, 255, 255)

        text = self.font.render(title, True, color)
        text_rect = text.get_rect(center=(self.window_width // 2, 25))
        self.screen.blit(text, text_rect)

    def solve_step(self):
        """Executa um passo do algoritmo backtracking."""
        if not self.stack:
            return False

        # Retirar posição da pilha
        current_pos = self.stack.pop()
        self.current_pos = current_pos
        current_row, current_col = current_pos

        # Se já visitou, pular
        if current_pos in self.visited:
            return True

        # Marcar como visitada
        self.visited.add(current_pos)

        # Verificar se encontrou o tesouro
        if self.maze[current_row][current_col] == 3:
            self.solution_path = self.reconstruct_path(current_pos)
            self.solved = True
            self.solving = False
            return False

        # Adicionar adjacentes à pilha
        adjacent = self.get_adjacent_positions(current_row, current_col)
        for pos in adjacent:
            if pos not in self.visited:
                self.stack.append(pos)
                self.parent[pos] = current_pos

        return len(self.stack) > 0

    def start_solving(self):
        """Inicia o processo de resolução."""
        if self.solving or self.solved:
            return

        # Reset
        self.stack = []
        self.visited = set()
        self.solution_path = []
        self.parent = {}
        self.current_pos = None
        self.solved = False

        # Encontrar início
        start, treasure = self.find_positions()
        if not start or not treasure:
            return

        # Iniciar algoritmo
        self.stack.append(start)
        self.parent[start] = None
        self.solving = True

    def reset(self):
        """Reseta o solucionador."""
        self.maze = [row[:] for row in self.original_maze]
        self.stack = []
        self.visited = set()
        self.solution_path = []
        self.parent = {}
        self.current_pos = None
        self.solving = False
        self.solved = False

    def handle_events(self):
        """Manipula eventos do Pygame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.start_solving()
                elif event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_UP:
                    self.speed = max(50, self.speed - 25)
                elif event.key == pygame.K_DOWN:
                    self.speed = min(500, self.speed + 25)

        return True

    def run(self):
        """Loop principal da aplicação."""
        clock = pygame.time.Clock()
        last_step_time = 0

        running = True
        while running:
            current_time = pygame.time.get_ticks()

            # Manipular eventos
            running = self.handle_events()

            # Executar passo do algoritmo
            if self.solving and current_time - last_step_time >= self.speed:
                if not self.solve_step():
                    self.solving = False
                last_step_time = current_time

            # Desenhar tudo
            self.screen.fill(self.colors['background'])
            self.draw_title()
            self.draw_maze()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


def generate_simple_maze(rows, cols):
    """Gera um labirinto simples."""
    maze = [[0 for _ in range(cols)] for _ in range(rows)]

    # Bordas são sempre paredes
    for i in range(rows):
        maze[i][0] = maze[i][cols - 1] = 0
    for j in range(cols):
        maze[0][j] = maze[rows - 1][j] = 0

    # Preencher interior
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if random.random() < 0.25:  # 25% chance de parede
                maze[i][j] = 0
            else:
                maze[i][j] = 1

    # Garantir início e fim
    maze[1][1] = 2  # Início
    maze[rows - 2][cols - 2] = 3  # Tesouro

    # Garantir pelo menos um caminho
    for i in range(1, rows - 1):
        maze[i][1] = 1
    for j in range(1, cols - 1):
        maze[rows - 2][j] = 1

    maze[1][1] = 2
    maze[rows - 2][cols - 2] = 3

    return maze


def main():
    """Função principal."""

    # Labirintos predefinidos
    labirinto_pequeno = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    labirinto_medio = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    print("=== SOLUCIONADOR DE LABIRINTO SIMPLES ===")
    print("\nEscolha o labirinto:")
    print("1 - Pequeno (8x8)")
    print("2 - Médio (12x12)")
    print("3 - Aleatório (15x15)")

    while True:
        try:
            escolha = input("\nDigite sua escolha (1-3): ").strip()

            if escolha == '1':
                labirinto = labirinto_pequeno
                cell_size = 60
                break
            elif escolha == '2':
                labirinto = labirinto_medio
                cell_size = 50
                break
            elif escolha == '3':
                labirinto = generate_simple_maze(15, 15)
                cell_size = 40
                break
            else:
                print("Escolha inválida! Digite 1, 2 ou 3.")

        except KeyboardInterrupt:
            print("\nSaindo...")
            return

    print(f"\nLabirinto carregado: {len(labirinto)}x{len(labirinto[0])}")
    print("\nCONTROLES:")
    print("SPACE - Iniciar resolução")
    print("R - Reset")
    print("UP/DOWN - Velocidade")
    print("ESC - Sair")

    print("\nCORES:")
    print("Preto - Paredes")
    print("Amarelo - Início")
    print("Laranja - Tesouro")
    print("Vermelho - Posição atual")
    print("Cinza - Visitado")
    print("Verde - Solução")

    try:
        solver = MazeSolverSimple(labirinto, cell_size=cell_size)
        solver.run()

    except Exception as e:
        print(f"\nErro: {e}")
        input("Pressione Enter para sair...")


if __name__ == "__main__":
    try:
        import pygame

        main()
    except ImportError:
        print("ERRO: Pygame não encontrado!")
        print("Para instalar: pip install pygame")
        input("Pressione Enter para sair...")
    except KeyboardInterrupt:
        print("\nPrograma interrompido.")
    except Exception as e:
        print(f"Erro: {e}")
        input("Pressione Enter para sair...")
        # Teste de commit
