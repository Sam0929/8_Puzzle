import random

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
            
if __name__ == "__main__":
    state_q1 = State()
    state_q1.display_state()
    print(state_q1.evaluate())
    state_q2 = state_q1.move('right')
    state_q2.display_state()
    state_q3 = state_q2.move('up')
    state_q3.display_state()
    state_q1.display_state()
    state_q2.display_state()
    state_q3.display_state()