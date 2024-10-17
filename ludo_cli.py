import random
import numpy as np
from rich.console import Console

console = Console()

class LudoGame:
    def __init__(self,  num_players, dice_till=6, pawns=4, difference=13, AUTO_ROLL_ENABLED=True, AUTO_PLAY_ENABLED=True):
        board_size = (max(4, num_players) * difference) +4    # 52 (+1) -2 +6 = 56
        self.rules = [num_players, dice_till, board_size, pawns, difference]
        self.ranks = []
        self.players = np.array([
            [
                [0] * pawns,    # position # till 50 + 6 steps
                [0] * pawns,    # tokens [# getting out tokens first 1 step, # issafe tokens safe zones, # reached home tokens last 6 steps]
            ]
            for x in range(num_players)
        ])
        self.colors = [
            "red", "green", "blue", "yellow", "magenta", "cyan", 
            "white", "bright_red", "bright_green", "bright_blue", 
            "bright_yellow", "bright_magenta", "bright_cyan"
        ]
        self.AUTO_ROLL_ENABLED = AUTO_ROLL_ENABLED 
        self.AUTO_PLAY_ENABLED = AUTO_PLAY_ENABLED

    def roll_dice(self):  return random.randint(1, self.rules[1])

    def check_movability(self, player_index, dice_roll) -> list:
        movable_pawns = []
        first_step_pawns = []

        if dice_roll != self.rules[1]:
            for i, j in enumerate(self.players[player_index, 1]):
                if j%10 ==1 and self.players[player_index, 0, i] + dice_roll <=self.rules[2]:
                    movable_pawns.append(i+1)

        else:
            for i, j in enumerate(self.players[player_index, 1]):
                if j%10 ==1:
                    if self.players[player_index, 0, i] + dice_roll <=self.rules[2]:
                        movable_pawns.append(i+1)
                else :
                    if self.players[player_index, 0, i] + dice_roll <=self.rules[2]:
                        first_step_pawns.append(i+1)

        return movable_pawns, first_step_pawns

    def check_token(self, number, position, digit = 1) -> bool:
        divisor = 10 ** (position)
        isolated_digit = (number // divisor) % 10
        return isolated_digit == digit

    def check_collision(self, pawn_index, player_index ):
        if self.players[player_index][1][pawn_index] == 1:
            pos = ((player_index*self.rules[4]) + self.players[player_index][0][pawn_index]) % (self.rules[2] - 4)
            same_pos = []
            for x,y in enumerate(self.players):
                if x!= player_index:
                    for i, j in enumerate(self.players[x][0]):
                        if pos == (((self.rules[4]*x)+self.players[x][0][i]) % (self.rules[2] - 4)) and self.players[x][1][i] == 1:
                            same_pos.append([x,i])
            if len(same_pos) == 1:
                player_index_collided, pawn_index_collided = same_pos[0][0], same_pos[0][1]
                self.players[player_index_collided][0][pawn_index_collided] = 0
                self.players[player_index_collided][1][pawn_index_collided] = 000
                print(f"P{player_index_collided + 1} pawn {pawn_index_collided + 1} sent home by P{player_index + 1} pawn {pawn_index + 1} ##################################################################################")
                return True
        return False
    
    def play_turn(self, player_index):
        spaces = ' '*42 * player_index
        if not self.AUTO_ROLL_ENABLED: input(f"{spaces}Enter to roll: ")
        dice_roll = self.roll_dice()
        movable_pawns, first_step_pawns = self.check_movability(player_index = player_index, dice_roll = dice_roll)
        console.print(f"{spaces} [bold {self.colors[player_index]}]P({player_index + 1}): {self.players[player_index][0]}[/bold {self.colors[player_index]}]", end=" ")
        # print(f"{spaces} P({player_index + 1}): {self.players[player_index][0]}", end=" ")
        console.print(f"[{self.colors[player_index]}] -- Dice: {dice_roll}[/ {self.colors[player_index]}]", )
    
        while True:
            try:
                if movable_pawns or first_step_pawns: 
                    if not AUTO_PLAY_ENABLED: 
                        pawn_index = int(input(f"{spaces} Movable Pawns {movable_pawns, first_step_pawns}. Enter which pawn: ")) - 1
                    else: 
                        print(f"{spaces} Movable Pawns {movable_pawns, first_step_pawns}. Enter which pawn: ")
                        pawn_index = (movable_pawns+first_step_pawns)[0] - 1
                    if pawn_index+1 in movable_pawns:
                        new_position = self.players[player_index][0][pawn_index] + dice_roll
                        self.players[player_index][0][pawn_index] = new_position

                        if new_position > self.rules[2] - 6:
                            self.players[player_index][1][pawn_index] = 111
                        elif (new_position % self.rules[4] in [0, 8]):
                            self.players[player_index][1][pawn_index] = 11
                        else:
                            self.players[player_index][1][pawn_index] = 1
                            
                        # print(f"{spaces} ----> {self.players[player_index][0]}")
                        console.print(f"[bold {self.colors[player_index]}]{spaces} ----> {self.players[player_index][0]}[/bold {self.colors[player_index]}]")
                        # if self.check_collision(pawn_index, player_index): print("colision")
                        break
                    elif pawn_index+1 in first_step_pawns:
                        self.players[player_index][1][pawn_index] = 11
                        # print(f"{spaces} ----> {self.players[player_index][0]}")
                        console.print(f"[bold {self.colors[player_index]}]{spaces} ----> {self.players[player_index][0]}[/bold {self.colors[player_index]}]")
                        break
                    else:
                        raise ValueError
                else:
                    break
            except ValueError:
                print(f"{spaces} Invalid input. Valid moves - {movable_pawns + first_step_pawns}")
            
        if all(x == self.rules[2] for x in self.players[player_index][0]) and (player_index +1 not in self.ranks):
            # input(f"Player {player_index + 1} wins!")
            console.print(f"{spaces}[bold {self.colors[player_index]}]Player {player_index + 1} wins![/bold {self.colors[player_index]}]")
            self.ranks.append(player_index + 1)
            if len(self.ranks) == self.rules[0] - 1:
                for i in range(1,self.rules[0]+1):
                    if i not in self.ranks:
                        # print(f"P{self.player_names[i]} lost the game!")
                        self.ranks.append(i)
                        break

                console.print(f"[bold bright_cyan]Winner Rankings:[/bold bright_cyan]")
                for i, rank in enumerate(self.ranks):
                    console.print(f"[bold bright_cyan]Rank {i + 1}: Player {rank}[/bold bright_cyan]")
                return True
        return False

    def play_game(self):
        player_index = 0
        while True:
            if self.play_turn(player_index):
                break
            player_index = (player_index + 1) % self.rules[0]
    
if __name__ == "__main__":
    num_players = int(input("Enter the number of players: "))
    if input("Do you want to enable auto roll? (y/n): ").lower() == "y":    AUTO_ROLL_ENABLED = True
    else:    AUTO_ROLL_ENABLED = False
    if input("Do you want to enable auto play (for DEBUG only)? (y/n): ").lower() == "y":    AUTO_PLAY_ENABLED = True
    else:    AUTO_PLAY_ENABLED = False
    
    game = LudoGame(num_players, AUTO_ROLL_ENABLED= AUTO_ROLL_ENABLED, AUTO_PLAY_ENABLED= AUTO_PLAY_ENABLED)
    game.play_game()




