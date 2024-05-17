import numpy as np

class Player:
  def __init__(self, name, strategy, chance_array=None):
    self.opponent_memory = []
    self.self_memory = []
    self.name = name
    self.total_score = 0
    self.strategy = strategy
    self.chance_array = chance_array
    self.chance_iter = 0

  def __str__(self):
    return f"{self.name} scored: {self.total_score}"
  
  def print_all(self):
    print(f"name: {self.name}\nscore: {self.total_score}\nopp_memory: {self.opponent_memory}\nself_memory: {self.self_memory}\nstrategy: {self.strategy}\nchance_array: {self.chance_array}\nchance_iter: {self.chance_iter}")

  def reset_memory(self):
    self.opponent_memory = []
    self.self_memory = []

  def reset_iterator(self):
    self.chance_iter = 0

  def reset(self):
    self.reset_memory()
    self.reset_iterator()

  def iterate_chance(self):
    self.chance_iter += 1

  
  def add_choices(self, opponents_choice, self_choice):
    self.opponent_memory.append(opponents_choice)
    self.self_memory.append(self_choice)
    if opponents_choice == "cooperate":
      if self_choice == "cooperate":
        self.add_score(3) # nice & nice = +3 points
      else:
        self.add_score(5) # nice & betrayed them = +5 points
    else:
      if self_choice == "cooperate":
        self.add_score(0) # defect & nice (was betrayed) = +0 points
      else:
        self.add_score(1) # defect & defect = +1 points
  
  def get_opponent_memory(self):
    return self.opponent_memory
  
  def get_self_memory(self):
    return self.self_memory
  
  def add_score(self, points):
    self.total_score += points
  
  def get_score(self):
    return self.total_score
  
  def get_choice(self):
    return self.strategy(self)

  '''
  IMPORTANT: chance entered is chance of 1's. Will be used as chance of defecting. a.k.a defecting = 1
  Takes a percent chance as a whole int i.e 20% = 20
  length_of_round is the length of the array you want to make based on the turns per match up of strategies
  i.e strategy 1 vs strategy 2 has 100 turns to "fight", that's a length_of_round = 100
  The point is to guarantee a percent chance will happen in a computer tournament setting

  For example Seeding a random < 10% wouldn't guarantee 10% at runtime.
  This does.
  '''
  def get_chance_array(percent_chance, length_of_round):
    output_array = []
    # Calculate elements
    num_ones = round(length_of_round * (percent_chance/100))
    num_zeros = length_of_round - num_ones
    
    # Populate array
    for zero in range(num_zeros):
      output_array.append(0)
    for one in range(num_ones):
      output_array.append(1)

    # Convert & shuffle array
    output_array = np.array(output_array)
    np.random.shuffle(output_array)

    return output_array
  
  def set_chance_array(self, chance_array):
    self.chance_array = chance_array

  def get_random_array_element(self):
    boolean_choice = self.chance_array[self.chance_iter]
    self.iterate_chance()
    return boolean_choice

  
  


def tit_for_tat(player):
  opp_memoy = player.get_opponent_memory()
  choice = None

  if len(opp_memoy) > 0:
    choice = opp_memoy[-1]
  else:
    choice = "cooperate"
  
  return choice

def good_guy(player):
  return "cooperate"

def bad_guy(player):
  return "defect"

def half_and_half(player):
  bool_choice = player.get_random_array_element()
  if bool_choice: # 1 == defect
    return "defect"
  else: # 0 == cooperate
    return "cooperate"
  
def get_players(number_of_turns):
  players = []
  players.append(Player('50/50', half_and_half, Player.get_chance_array(50, number_of_turns)))
  players.append(Player('jesus', good_guy))
  players.append(Player('devil', bad_guy))
  players.append(Player('tit_for_tat', tit_for_tat))

  return players
  



def main():
  ROUND_LENGTH = 20
  fifty_fifty = Player('50/50', half_and_half, Player.get_chance_array(50, ROUND_LENGTH))
  fifty_fifty.print_all()
  print(fifty_fifty.get_choice())
  fifty_fifty.print_all()
  print(fifty_fifty.get_choice())

if __name__ == "__main__":
  main()