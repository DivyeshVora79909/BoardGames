import random
from rich.console import Console
console = Console()

class SnakeAndLaddersGame:
    def __init__(self, num_players, AUTO_ROLL_ENABLED=False):
        console.print("Welcome to Snake and Ladders!")

        self.num_players = num_players
        self.player_positions = [0] * num_players
        self.player_names = [i+1 for i in range(num_players)]
        self.current_player = 0
        self.finished_players = []
        self.spaces = " "
        self.board = {
            4: 14,    9: 31,    20: 38,    28: 84,    40: 59,    51: 67,    63: 81,    71: 91,    # ladders
            87: 24,    93: 73,    64: 60,    95: 75,    99: 78,    62: 19,    54: 34,    17: 7,    # snakes
        }
        self.colors = [
            "red", "green", "blue", "yellow", "magenta", "cyan", 
            "white", "bright_red", "bright_green", "bright_blue", 
            "bright_yellow", "bright_magenta", "bright_cyan"
        ]
        self.AUTO_ROLL_ENABLED = AUTO_ROLL_ENABLED

    def roll_die(self):
        return random.randint(1, 6)

    def move_player(self, current_position, steps):
        new_position = current_position + steps
        if new_position in self.board:
            new_position = self.board[new_position]
        return new_position

    def has_won(self, position):
        return position == 100

    def check_collisions(self, current_player):
        current_position = self.player_positions[current_player]
        for i, position in enumerate(self.player_positions):
            if i != current_player and position == current_position and position != 100:
                self.player_positions[i] = max(0, self.player_positions[i] - 5)
                console.print(f"[bold {self.colors[current_player]}]{self.player_names[current_player]} collided with {self.player_names[i]}, so {self.player_names[i]} moved back 5 steps[/bold {self.colors[current_player]}]")
                break

    def play_turn(self):
        if not self.AUTO_ROLL_ENABLED:
            input(f"{self.spaces * self.current_player * 45}P{self.player_names[self.current_player]}, press Enter to roll the die...")
        steps = self.roll_die()
        console.print(f"[bold {self.colors[self.current_player]}]{self.spaces * self.current_player * 45}P{self.player_names[self.current_player]} rolled -> {steps}[/bold {self.colors[self.current_player]}]")

        if self.player_positions[self.current_player] + steps <= 100:   # Check if the move is valid
            self.player_positions[self.current_player] = self.move_player(self.player_positions[self.current_player], steps)
            console.print(f"[bold {self.colors[self.current_player]}]{self.spaces * self.current_player * 45}position --> {self.player_positions[self.current_player]}[/bold {self.colors[self.current_player]}]")
            # print(f"{self.spaces * self.current_player * 45}{self.player_names[self.current_player]} --> {self.player_positions[self.current_player]}")

            # Check for collisions
            self.check_collisions(self.current_player)

            if self.has_won(self.player_positions[self.current_player]) and self.current_player not in self.finished_players:
                self.finished_players.append(self.current_player)
                console.print(f"[bold {self.colors[self.current_player]}]{self.spaces * self.current_player * 45}P{self.player_names[self.current_player]} has finished the game![/bold {self.colors[self.current_player]}]")
        else:
            console.print(f"[bold {self.colors[self.current_player]}]{self.spaces * self.current_player * 45}{self.player_names[self.current_player]} cannot move as it exceeds 100. Skipping turn[/bold {self.colors[self.current_player]}]")

        while steps == 6:
            if not self.AUTO_ROLL_ENABLED:
                input(f"{self.spaces * self.current_player * 45}P{self.player_names[self.current_player]}, you rolled a 6! Press Enter to roll again...")
            steps = self.roll_die()
            console.print(f"[bold {self.colors[self.current_player]}]{self.spaces * self.current_player * 45}P{self.player_names[self.current_player]} rolled -> {steps}[/bold {self.colors[self.current_player]}]")

            if self.player_positions[self.current_player] + steps <= 100:
                self.player_positions[self.current_player] = self.move_player(self.player_positions[self.current_player], steps)
                console.print(f"{self.spaces * self.current_player * 45}position --> {self.player_positions[self.current_player]}")
                # print(f"{self.spaces * self.current_player * 45}{self.player_names[self.current_player]}position --> {self.player_positions[self.current_player]}")

                self.check_collisions(self.current_player)

                if self.has_won(self.player_positions[self.current_player]) and self.current_player not in self.finished_players:
                    self.finished_players.append(self.current_player)
                    print(f"{self.spaces * self.current_player * 45}P{self.player_names[self.current_player]} has finished the game!")
            else:
                console.print(f"[bold {self.colors[self.current_player]}]{self.spaces * self.current_player * 45}P{self.player_names[self.current_player]} cannot move. Skipping turn[/bold {self.colors[self.current_player]}]")
                # print(f"{self.spaces * self.current_player * 45}P{self.player_names[self.current_player]} cannot move as it exceeds 100. Skipping turn")

    def switch_player(self):
        self.current_player = (self.current_player + 1) % self.num_players
        while self.current_player in self.finished_players:
            self.current_player = (self.current_player + 1) % self.num_players

    def determine_loser(self):
        for i in range(self.num_players):
            if i not in self.finished_players:
                print(f"P{self.player_names[i]} lost the game!")
                self.finished_players.append(i)
                break

    def assign_ranks(self):
        console.print("\nFinal Ranks:")
        for rank, player in enumerate(self.finished_players, start=1):
            console.print(f"[bold {self.colors[-1]}]Rank {rank}: P{self.player_names[player]} --> Position: {self.player_positions[player]}[/bold {self.colors[-1]}]")

    def play_game(self):
        # print(f"Welcome to the game! There are {self.player_names} players.")
        while len(self.finished_players) < self.num_players - 1:
            self.play_turn()
            self.switch_player()
        self.determine_loser()
        self.assign_ranks()

if __name__ == "__main__":
    # print("Welcome to Snake and Ladders!")
    # num_players = int(input("Enter the number of players: "))
    num_players = int(input("Enter the number of players: "))
    AUTO_ROLL_ENABLED = input("Do you want to enable automatic rolling? (y/n): ").lower() == 'y'

    game = SnakeAndLaddersGame(num_players=num_players, AUTO_ROLL_ENABLED=AUTO_ROLL_ENABLED)
    game.play_game()

