from player import Player
from player import get_players
import matplotlib.pyplot as plt

def run_simulation(number_of_turns, main_players, opponent_players):

  for player1 in main_players: # Only keep player 1's score but both are about equal
    for player2 in opponent_players:
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

def display_graph(names, scores):
  fig, ax = plt.subplots(figsize=(15, 10))
  bar_container = ax.bar(names, scores)
  ax.set(ylabel='Total points scored', title='LongView Prisoners Dilemma Tournament')
  ax.bar_label(bar_container, scores)
  plt.show()


def main():
  number_of_turns = int(input("Enter the number of turns per round: "))

  players_1 = get_players(number_of_turns)
  players_2 = get_players(number_of_turns)
  run_simulation(number_of_turns, players_1, players_2)

  names_list = []
  score_list = []
  for player in players_1:
    names_list.append(player.name)
    score_list.append(player.total_score)

  results = {}  # In able to print the winners (probably a better way to do this)
  for i, name in enumerate(names_list): #create hash map
    results[name] = score_list[i]
  for key, value in sorted(results.items(), key=lambda x: x[1], reverse=True):  # Print most to least points
    print("{} : {}".format(key, value))

  display_graph(names_list, score_list)
  
    

if __name__ == '__main__':
  main()