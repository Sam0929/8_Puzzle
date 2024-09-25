import random
import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu
from collections import deque

class State:
    def __init__(self, state=None, empty_tile_index=None, moves=None, level=0):
        """Inicializa o estado do quebra-cabeça."""
        if state is None and empty_tile_index is None:
            self.state, self.empty_tile_index = self.create_state()
            self.level = level
        else:
            self.state = state
            self.empty_tile_index = empty_tile_index
            self.level = level
        self.f = 0
        self.moves = moves if moves is not None else []

    def evaluate(self) -> bool:
        """Verifica se o estado atual é o estado final do quebra-cabeça."""
        final_state = [[1, 2, 3], [4, 5, 6], [7, 8, "X"]]
        return self.state == final_state

    def create_state(self):
        """Cria um estado inicial aleatório do quebra-cabeça."""
        state = list(range(9))
        random.shuffle(state)
        while not self.is_solvable(state):
            random.shuffle(state)
        empty_tile_index = next(index for index, num in enumerate(state) if num == 0)
        state[empty_tile_index] = 'X'  # Representa a posição vazia
        return [state[i:i+3] for i in range(0, 9, 3)], empty_tile_index

    def is_solvable(self, state):
        """Verifica se o estado do quebra-cabeça é solucionável."""
        flat_state = [num for num in state if num != 0]
        inversions = 0
        for i in range(len(flat_state)):
            for j in range(i + 1, len(flat_state)):
                if flat_state[i] > flat_state[j]:
                    inversions += 1
        return inversions % 2 == 0
    
    def display_state(self):
        """Exibe o estado atual do quebra-cabeça no console."""
        for row in self.state:
            print(row)
    
    def move(self, direction: str):
        """Executa um movimento na direção especificada."""
        flat_state = [item for sublist in self.state for item in sublist]
        new_empty_tile_index = self.empty_tile_index

        # Verifica a validade do movimento
        if direction == 'up' and self.empty_tile_index >= 3:
            new_empty_tile_index = self.empty_tile_index - 3
        elif direction == 'down' and self.empty_tile_index <= 5:
            new_empty_tile_index = self.empty_tile_index + 3
        elif direction == 'left' and self.empty_tile_index % 3 != 0:
            new_empty_tile_index = self.empty_tile_index - 1
        elif direction == 'right' and self.empty_tile_index % 3 != 2:
            new_empty_tile_index = self.empty_tile_index + 1
        else:
            return None  # Movimento inválido
        
        # Cria um novo estado após o movimento
        new_flat_state = flat_state.copy()
        new_flat_state[self.empty_tile_index], new_flat_state[new_empty_tile_index] = (
            new_flat_state[new_empty_tile_index], new_flat_state[self.empty_tile_index]
        )
        new_state = [new_flat_state[i:i+3] for i in range(0, 9, 3)]
        return State(new_state, new_empty_tile_index, self.moves + [direction])

    @staticmethod
    def bfs(initial_state):
        """Busca a solução usando o algoritmo BFS."""
        queue = deque([initial_state])
        visited = set()
        visited.add(tuple([item for sublist in initial_state.state for item in sublist]))
        
        visited_count = 0  # Contador de estados visitados
        
        while queue:
            current_state = queue.popleft()
            visited_count += 1  # Incrementar a cada estado retirado da fila
            
            if current_state.evaluate():
                return current_state.moves, visited_count  # Retorna a sequência de movimentos e a contagem de estados visitados
            
            for direction in ['up', 'down', 'left', 'right']:
                new_state = current_state.move(direction)
                if new_state:
                    flat_state = tuple([item for sublist in new_state.state for item in sublist])
                    if flat_state not in visited:
                        visited.add(flat_state)
                        queue.append(new_state)

        return None, visited_count  # Retorna a contagem mesmo se não encontrar solução
    
    @staticmethod
    def dfs(initial_state: "State", max_depth=50):
        """Busca a solução usando o algoritmo DFS."""
        stack = [(initial_state, 0)]  # Pilha com (estado, profundidade)
        visited = set()
        visited.add(tuple([item for sublist in initial_state.state for item in sublist]))
        
        visited_count = 0  # Contador de estados visitados

        while stack:
            current_state, depth = stack.pop()
            visited_count += 1  # Incrementar a cada estado retirado da pilha

            if current_state.evaluate():
                return current_state.moves, visited_count  # Retorna a sequência de movimentos e a contagem de estados visitados

            if depth < max_depth:  # Limite de profundidade
                for direction in ['up', 'down', 'left', 'right']:
                    new_state = current_state.move(direction)
                    if new_state:
                        flat_state = tuple([item for sublist in new_state.state for item in sublist])
                        if flat_state not in visited:
                            visited.add(flat_state)
                            stack.append((new_state, depth + 1))

        return None, visited_count  # Retorna a contagem mesmo se não encontrar solução

    @staticmethod
    def a_star(start):
        """Busca a solução usando o algoritmo A*."""
        start.f = State.heuristic(start)
        open_list = []
        closed_list = []
        open_list.append(start)
        visited_count = 0

        while open_list:
            current_state = open_list.pop(0)
            visited_count += 1

            # Verifica se o estado atual é o objetivo
            if current_state.evaluate():
                return current_state.moves, visited_count

            closed_list.append(current_state)

            # Gera os filhos do estado atual
            children = []
            for direction in ["up", "down", "left", "right"]:
                new_state = current_state.move(direction)
                if new_state is not None:
                    children.append(new_state)

            for child in children:
                child.f = State.heuristic(child)

                if any(closed_child.state == child.state for closed_child in closed_list):
                    continue

                if any(open_node.state == child.state and child.f >= open_node.f for open_node in open_list):
                    continue

                open_list.append(child)
            open_list.sort(key=lambda x: x.f)

    @staticmethod
    def heuristic(state):
        """Calcula a heurística usando a distância de Manhattan."""
        goal = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1), "X": (2, 2)
        }
        
        h = 0

        for i in range(3):
            for j in range(3):
                value = state.state[i][j]
                if value != 'X':  # Ignora a posição vazia ('X')
                    goal_position = goal[value]
                    h += abs(i - goal_position[0]) + abs(j - goal_position[1])

        return h + state.level

import tkinter as tk
from tkinter import messagebox, StringVar, OptionMenu

class PuzzleGUI:
    def __init__(self, master):
        """Inicializa a interface gráfica do quebra-cabeça."""
        self.master = master
        self.master.title("Puzzle Game")
        self.state = State()  # Estado inicial embaralhado
        self.initial_state = self.state  # Salva o estado inicial para reiniciar
        self.create_widgets()
        self.update_display()
        self.bind_keys()

    def create_widgets(self):
        """Cria os botões e elementos da interface gráfica."""
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                btn = tk.Button(self.master, text="", width=10, height=4, command=lambda r=r, c=c: self.on_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

        self.up_button = tk.Button(self.master, text="Cima", command=self.move_up)
        self.down_button = tk.Button(self.master, text="Baixo", command=self.move_down)
        self.left_button = tk.Button(self.master, text="Esquerda", command=self.move_left)
        self.right_button = tk.Button(self.master, text="Direita", command=self.move_right)

        self.solve_var = StringVar(value="Resolver")
        self.solve_dropdown = OptionMenu(self.master, self.solve_var, "BFS", "DFS", "A*", command=self.solve_puzzle)
        self.restart_button = tk.Button(self.master, text="Reiniciar", command=self.restart_game)

        self.up_button.grid(row=3, column=1)
        self.down_button.grid(row=4, column=1)
        self.left_button.grid(row=3, column=0)
        self.right_button.grid(row=3, column=2)
        self.solve_dropdown.grid(row=5, column=1)
        self.restart_button.grid(row=6, column=1)

    def update_display(self):
        """Atualiza a exibição do estado atual do quebra-cabeça."""
        for r in range(3):
            for c in range(3):
                value = self.state.state[r][c]
                self.buttons[r][c].config(text=value if value != 'X' else "", bg="lightblue" if value == 'X' else "white")

    def move_up(self):
        """Move a peça vazia para cima se possível."""
        new_state = self.state.move('up')
        if new_state:
            self.state = new_state
            self.update_display()
            self.check_win()

    def move_down(self):
        """Move a peça vazia para baixo se possível."""
        new_state = self.state.move('down')
        if new_state:
            self.state = new_state
            self.update_display()
            self.check_win()

    def move_left(self):
        """Move a peça vazia para a esquerda se possível."""
        new_state = self.state.move('left')
        if new_state:
            self.state = new_state
            self.update_display()
            self.check_win()

    def move_right(self):
        """Move a peça vazia para a direita se possível."""
        new_state = self.state.move('right')
        if new_state:
            self.state = new_state
            self.update_display()
            self.check_win()

    def bind_keys(self):
        """Vincula as teclas para movimentação do quebra-cabeça."""
        self.master.bind('<w>', self.move_up_key)
        self.master.bind('<s>', self.move_down_key)
        self.master.bind('<a>', self.move_left_key)
        self.master.bind('<d>', self.move_right_key)

    def move_up_key(self, event):
        """Movimento para cima usando a tecla 'w'."""
        self.move_up()

    def move_down_key(self, event):
        """Movimento para baixo usando a tecla 's'."""
        self.move_down()

    def move_left_key(self, event):
        """Movimento para a esquerda usando a tecla 'a'."""
        self.move_left()

    def move_right_key(self, event):
        """Movimento para a direita usando a tecla 'd'."""
        self.move_right()

    def check_win(self):
        """Verifica se o jogador venceu."""
        if self.state.evaluate():
            self.show_win_message()

    def show_win_message(self):
        """Exibe uma mensagem de vitória."""
        messagebox.showinfo("Parabéns!", "Você venceu!")

    def restart_game(self, state=None):
        """Reinicia o jogo com um novo estado ou com o estado inicial."""
        if state is not None:
            self.state = state
        else:
            self.state = State()  # Reinicia com um novo estado aleatório
        self.update_display()

    def solve_puzzle(self, method):
        """Inicia a resolução do quebra-cabeça com o método selecionado."""
        current_state = State(self.state.state, self.state.empty_tile_index)  # Use o índice da peça vazia
        if method == "BFS":
            solution, visited_count = State.bfs(current_state)
        elif method == "DFS":
            solution, visited_count = State.dfs(current_state)
        elif method == "A*":
            solution, visited_count = State.a_star(current_state)

        if solution:
            self.show_solution_window(solution, visited_count)
        else:
            messagebox.showinfo("Solução", f"Nenhuma solução foi encontrada.\nEstados visitados: {visited_count}")

    def show_solution_window(self, solution, visited_count):
        """Exibe a janela de solução encontrada."""
        win_message = tk.Toplevel(self.master)
        win_message.title("Solução encontrada!")

        message_label = tk.Label(win_message, text=f"Solução: {solution}\n Encontrada com {len(solution)} movimentos.\nEstados visitados: {visited_count}", padx=20, pady=20)
        message_label.pack()

        speed_label = tk.Label(win_message, text="Velocidade de resolução (ms por movimento):")
        speed_label.pack(pady=5)

        speed_slider = tk.Scale(win_message, from_=100, to=2000, orient='horizontal')
        speed_slider.set(500)  # Velocidade padrão (500 ms)
        speed_slider.pack(pady=5)

        auto_solve_button = tk.Button(win_message, text="Resolver automaticamente", 
                                       command=lambda: [self.close_and_auto_solve(win_message, solution, speed_slider.get())])
        auto_solve_button.pack(pady=10)

        close_button = tk.Button(win_message, text="Fechar", command=win_message.destroy)
        close_button.pack(pady=10)

    def close_and_auto_solve(self, win_message, solution, speed):
        """Fecha a janela de solução e inicia a resolução automática."""
        win_message.destroy()  # Fecha a janela
        self.auto_solve(solution, speed)  # Inicia a resolução automática

    def auto_solve(self, solution, speed):
        """Executa a solução automática com base na sequência de movimentos."""
        def perform_moves(index=0):
            if index < len(solution):
                direction = solution[index]
                if direction == 'up':
                    self.move_up()
                elif direction == 'down':
                    self.move_down()
                elif direction == 'left':
                    self.move_left()
                elif direction == 'right':
                    self.move_right()

                # Chama o próximo movimento após um intervalo de tempo
                self.master.after(speed, perform_moves, index + 1)
            else:
                # Exibe a mensagem após a solução completa
                messagebox.showinfo("Solução Completa", "O quebra-cabeça foi resolvido automaticamente!")
                self.restart_game(self.initial_state)  # Reinicia o jogo com estado inicial

        # Inicia o processo de resolução automática
        perform_moves()



if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()
