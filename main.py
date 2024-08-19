import random
import tkinter as tk
class State:
    def __init__(self, state = None, x_index = None):
        if state is None and x_index is None:
            self.state, self.x_index = self.create_state()
        else:
            self.state = state
            self.x_index = x_index

    def evaluate(self) -> bool:
        final_state = [[1, 2, 3], [4, 5, 6], [7, 8, "X"]]
        flat_state = [item for sublist in self.state for item in sublist]
        flat_final_state = [item for sublist in final_state for item in sublist]

        return flat_state == flat_final_state

    def create_state(self):
        state = list(range(9))
        random.shuffle(state)
        while not self.is_solvable(state):
            random.shuffle(state)
            
        x_index = next(index for index, num in enumerate(state) if num == 0)
        state[x_index] = 'X'
        return [state[i:i+3] for i in range(0, 9, 3)], x_index

    def is_solvable(self, state):
        flat_state = [num for num in state if num != 0]
        inversions = 0
        for i in range(len(flat_state)):
            for j in range(i + 1, len(flat_state)):
                if flat_state[i] > flat_state[j]:
                    inversions += 1
        return inversions % 2 == 0

    def display_state(self):
        for row in self.state:
            print(row)
            
    def move(self, direction: str):
        flat_state = [item for sublist in self.state for item in sublist]
        if direction == 'up' and self.x_index >= 3:
            new_x_index = self.x_index - 3
        elif direction == 'down' and self.x_index <= 5:
            new_x_index = self.x_index + 3
        elif direction == 'left' and self.x_index % 3 != 0:
            new_x_index = self.x_index - 1
        elif direction == 'right' and self.x_index % 3 != 2:
            new_x_index = self.x_index + 1
        else:
            print("Movimento inválido")
            return self

        new_flat_state = flat_state.copy()
        new_flat_state[self.x_index], new_flat_state[new_x_index] = new_flat_state[new_x_index], new_flat_state[self.x_index]
        new_state = [new_flat_state[i:i+3] for i in range(0, 9, 3)]
        return State(new_state, new_x_index)
            
class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Puzzle Game")

        self.state = State()
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                btn = tk.Button(self.master, text="", width=10, height=4, command=lambda r=r, c=c: self.on_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

        self.up_button = tk.Button(self.master, text="Up", command=self.move_up)
        self.down_button = tk.Button(self.master, text="Down", command=self.move_down)
        self.left_button = tk.Button(self.master, text="Left", command=self.move_left)
        self.right_button = tk.Button(self.master, text="Right", command=self.move_right)

        self.up_button.grid(row=3, column=1)
        self.down_button.grid(row=4, column=1)
        self.left_button.grid(row=3, column=0)
        self.right_button.grid(row=3, column=2)

    def update_display(self):
        for r in range(3):
            for c in range(3):
                value = self.state.state[r][c]
                self.buttons[r][c].config(text=value if value != 'X' else "", bg="lightblue" if value == 'X' else "white")

    def on_click(self, row, col):
        # Dummy function for cell click, as we are using buttons for movement
        pass

    def move_up(self):
        new_state = self.state.move('up')
        if new_state:
            self.state = new_state
            self.update_display()

    def move_down(self):
        new_state = self.state.move('down')
        if new_state:
            self.state = new_state
            self.update_display()

    def move_left(self):
        new_state = self.state.move('left')
        if new_state:
            self.state = new_state
            self.update_display()

    def move_right(self):
        new_state = self.state.move('right')
        if new_state:
            self.state = new_state
            self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleGUI(root)
    root.mainloop()