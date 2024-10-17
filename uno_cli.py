
import sys
import random

class UnoGame:
    def __init__(self, players=3, cards_per_player=3, autoplay = False):
        self.deck = {
            '00': 'red0', '01': 'red1', '02': 'red2', '03': 'red3', '04': 'red4', '05': 'red5', '06': 'red6', '07': 'red7', '08': 'red8', '09': 'red9', '10': 'redskip', '11': 'redreverse', '12': 'red+2', 
            '13': 'blue0', '14': 'blue1', '15': 'blue2', '16': 'blue3', '17': 'blue4', '18': 'blue5', '19': 'blue6', '20': 'blue7', '21': 'blue8', '22': 'blue9', '23': 'blueskip', '24': 'bluereverse', '25': 'blue+2', 
            '26': 'green0', '27': 'green1', '28': 'green2', '29': 'green3', '30': 'green4', '31': 'green5', '32': 'green6', '33': 'green7', '34': 'green8', '35': 'green9', '36': 'greenskip', '37': 'greenreverse', '38': 'green+2', 
            '39': 'yellow0', '40': 'yellow1', '41': 'yellow2', '42': 'yellow3', '43': 'yellow4', '44': 'yellow5', '45': 'yellow6', '46': 'yellow7', '47': 'yellow8', '48': 'yellow9', '49': 'yellowskip', '50': 'yellowreverse', '51': 'yellow+2', 
            '52': 'wild', '53': 'wild +4', '54': 'wild', '55': 'wild2 +4',
        }

        self.autoplay = autoplay
        self.players = players
        self.cards_per_player = cards_per_player
        self.deck_encoded = list(self.deck.keys())
        self.decks_required = ((self.players * self.cards_per_player + 40) // len(self.deck_encoded)) + 1
        self.play_deck = self.deck_encoded * self.decks_required
        random.shuffle(self.play_deck)

        self.player_cards = []
        self.played_pile = []
        self.pile = []
        self.current_player = 0
        self.ranks = []

        self.direction = 1  # reverse card flag
        self.skip_next = False  # skip card flag
        self.draw_2 = False  # draw 2 card flag
        self.draw_4 = False  # draw 4 card flag

        self.spaces = " "*40

        self.distribute_cards()
        self.initialize_game()

    def distribute_cards(self):
        """Distribute cards to each player"""
        for i in range(self.players):
            self.player_cards.append(self.play_deck[i * self.cards_per_player:i * self.cards_per_player + self.cards_per_player])
            if i == self.players - 1:
                self.pile = self.play_deck[i * self.cards_per_player + self.cards_per_player:]

    def initialize_game(self):
        """Initialize the game with the first played card"""
        self.played_pile.append(self.pile.pop())

    def reshuffle_pile(self):
        """Reshuffle the pile if it runs low"""
        if len(self.pile) < 5 and len(self.played_pile) > 20:
            self.pile.extend(self.played_pile[-20:])
            self.played_pile = self.played_pile[:-20]
            random.shuffle(self.pile)

    def get_playable_cards(self, cards):
        """Return a list of playable cards based on the top of the played pile"""
        top_card = self.played_pile[-1]
        playable_cards = [card for card in cards if int(card) > 51 or 
                          (int(card) // 13 == int(top_card) // 13) or 
                          (abs(int(card) - int(top_card)) % 13 == 0) or 
                          int(top_card) > 51]
        return playable_cards

    def play_turn(self):
        """Handles the logic of a single turn for the current player"""
        if self.skip_next:
            print(f"{self.spaces*self.current_player}P{self.current_player+1} skipped")
            self.skip_next = False
            return
        
        if self.draw_2:
            print(f"{self.spaces*self.current_player}P{self.current_player+1} drew 2 cards")
            self.draw_2 = False
            self.player_cards[self.current_player].append(self.pile.pop())
            self.player_cards[self.current_player].append(self.pile.pop())

        if self.draw_4:
            print(f"{self.spaces*self.current_player}P{self.current_player+1} drew 2 cards")
            self.draw_4 = False
            self.player_cards[self.current_player].append(self.pile.pop())
            self.player_cards[self.current_player].append(self.pile.pop())
            self.player_cards[self.current_player].append(self.pile.pop())
            self.player_cards[self.current_player].append(self.pile.pop())

        cards = self.player_cards[self.current_player]

        if cards:
            playable_cards = self.get_playable_cards(cards)

            if playable_cards:
                print(f"{self.spaces*self.current_player}P{self.current_player+1} turn. Top of pile {self.deck[self.played_pile[-1]]}")
                while True:
                    try:
                        print(f"{self.spaces*self.current_player}Cards: {[self.deck[x] for x in cards]}")
                        if not self.autoplay: inp = int(input(f"{self.spaces*self.current_player}Playable Cards {[self.deck[x] for x in playable_cards]} for {self.played_pile[-1]}. Enter indexes in {[x for x in range(len(playable_cards))]}: "))
                        else: inp = 0
                        # if inp == 100: sys.exit()
                        if 0 <= inp < len(playable_cards):
                            print(f"{self.spaces*self.current_player}P{self.current_player+1} played {self.deck[playable_cards[inp]]}")
                            self.played_pile.append(playable_cards[inp])
                            self.player_cards[self.current_player].remove(playable_cards[inp])

                            if int(self.played_pile[-1]) % 13 == 12:  # check for +2 card
                                print(f"{self.spaces*self.current_player}Draw +2 card played! +2 for next player.")
                                self.draw_2 = True

                            elif int(self.played_pile[-1]) % 13 == 11:  # If the card played is a reverse card # check for reverse card
                                print(f"{self.spaces*self.current_player}Reverse card played! Reversing direction.")
                                self.direction *= -1

                            elif int(self.played_pile[-1]) % 13 == 10:  # check for skip card
                                print(f"{self.spaces*self.current_player}Skip card played! Skiping next player.")
                                self.skip_next = True

                            elif int(self.played_pile[-1]) in [55,53]:  # check for +4 card
                                print(f"{self.spaces*self.current_player}Skip card played! Skiping next player.")
                                self.draw_4 = True

                            break
                        else:
                            raise ValueError("Invalid input")
                    except ValueError:
                        print(f"{self.spaces*self.current_player}Invalid input. Valid input: {[x for x in range(len(playable_cards))]} --------")
                
                if not cards:
                    self.ranks.append(self.current_player)
                    print(f"{self.spaces*self.current_player}P{self.current_player+1} won ##########")
            else:
                print(f"{self.spaces*self.current_player}P{self.current_player+1} turn. Top of pile {self.played_pile[-1]}")
                print(f"{self.spaces*self.current_player}No cards to play, drawing from pile.")
                self.player_cards[self.current_player].append(self.pile.pop())

        else:
            print(f"{self.spaces*self.current_player}P{self.current_player+1} already won.")

    def check_game_over(self):
        """Check if the game is over (all players but one have won)"""
        return len(self.ranks) == self.players - 1

    def next_player(self):
        """Move to the next player"""
        # self.current_player = (self.current_player + 1) % self.players
        self.current_player = (self.current_player + self.direction + self.players) % self.players

    def start_game(self):
        """Main game loop"""
        while not self.check_game_over():
            self.reshuffle_pile()
            self.play_turn()
            self.next_player()

        print("\n######## Final Rankings: ########")
        for rank, player in enumerate(self.ranks):
            print(f"{rank+1}st: Player {player+1}")

        remaining_player = (set(range(self.players)) - set(self.ranks)).pop()
        print(f"Last: Player {remaining_player+1}")


if __name__ == "__main__":
    players = int(input("Enter the number of players: "))
    cards_per_player = int(input("Enter the number of cards per player: "))
    AUTO_PLAY = bool(input("For debug purposes => \n\tEnter any value for Auto play, else just enter for normal play: "))
    
    game = UnoGame(players=players, cards_per_player=cards_per_player, autoplay=AUTO_PLAY)
    game.start_game()




