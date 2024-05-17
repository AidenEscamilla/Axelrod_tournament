from player import Player
from player import get_players
def main():
  number_of_turns = int(input("Enter the number of turns per round: "))

  players_1 = get_players(number_of_turns)
  players_2 = get_players(number_of_turns)
  for player1 in players_1: # Only keep player 1's score but both are about equal
    for player2 in players_2:
      print(f"{player1.name} vs {player2.name}")
      # Play rounds against each other
      for _ in range(number_of_turns):
        choice1 = player1.get_choice()
        choice2 = player2.get_choice()
        player1.add_choices(choice2, choice1)
        player2.add_choices(choice1, choice2)
      # Reset memory and iterator for next opponent
      player2.reset()
      player1.reset()
  
  for player in players_1:
    print(f"{player.name}: {player.total_score}")

    

if __name__ == '__main__':
  main()