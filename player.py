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
    self.temp_strat = None

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
  
  def set_temp_strat(self, strat_to_remember):
    self.temp_strat = strat_to_remember

  def get_temp_strat_result(self):
    return self.temp_strat(self)

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
  
  '''
  IMPORTANT: This does not require 0's and 1's. The array could just be 'defect' or 'cooperate'.
  Make sure you know how you're implementing this function.
  choice_pattern is an array with a set pattern that is want to be repeated.
  This function takes that array, and the number of rounds, and repeates said pattern.
  Note: Patterns that don't divide evenly into the number of rounds are truncated and appended to the end
  '''
  def get_choice_pattern_array(choice_pattern, length_of_round):
    output_array = []
    # Calculate elements
    number_of_full_patterns = length_of_round // len(choice_pattern)
    partial_pattern_length = length_of_round % len(choice_pattern)

    for _ in range(number_of_full_patterns):
      output_array.extend(choice_pattern)
    if partial_pattern_length > 0:  # Guard against adding an extra element 
      output_array.extend(choice_pattern[:partial_pattern_length])  # Only add up to the cut-off
  
    return output_array
  
  def set_chance_array(self, chance_array):
    self.chance_array = chance_array

  def get_next_array_element(self):
    boolean_choice = self.chance_array[self.chance_iter]
    self.iterate_chance()
    return boolean_choice

  
  

# Strategies

def tit_for_tat(player):
  opp_memory = player.get_opponent_memory()
  choice = None

  if len(opp_memory) > 0:
    choice = opp_memory[-1]
  else:
    choice = "cooperate"
  
  return choice

def inverse_tit_for_tat(player):
  opp_memory = player.get_opponent_memory()
  choice = None

  if len(opp_memory) > 0:
    opp_last_choice = opp_memory[-1]
    # Choose oppositer of what they did last round
    if opp_last_choice == "cooperate":
      choice = "defect" 
    else:
      choice = "cooperate"
  
  else: # 1st choice defect
    choice = "defect"

  return choice

def good_guy(player):
  return "cooperate"

def bad_guy(player):
  return "defect"

def random_or_preset_choices(player):
  bool_choice = player.get_next_array_element()
  if bool_choice: # 1 == defect
    return "defect"
  else: # 0 == cooperate
    return "cooperate" 
  
def heart_of_iron_4(player):
  # cases where it's not tit_for_tat
  edge_case_1_1 = ["cooperate","defect","cooperate","defect","defect", "cooperate", "cooperate"]
  edge_case_1_2 = ["cooperate","defect","cooperate","defect","defect", "cooperate", "defect"]
  edge_case_1_3 = ["cooperate","defect","cooperate","defect","defect", "defect", "defect"]
  # Cases where it's not myself
  edge_case_2_1 = ["defect","cooperate","defect","defect","defect", "defect", "defect"]
  edge_case_2_2 = ["defect","cooperate","defect","defect","defect", "cooperate", "defect"]
  edge_case_2_3 = ["defect","cooperate","defect","defect","defect", "defect", "cooperate"]

  opp_memory = player.get_opponent_memory()
  mode = None
  #round_number = len(self_memory) # Why would I add this here? What're the advantages to this?
  if len(opp_memory) in [0, 2, 3, 4]: # rounds 1,3,4,5
    return "defect"
  elif len(opp_memory) == 1: #round 2
    return "cooperate"
  
  if opp_memory[:5] == ["defect","cooperate","defect","defect","defect"]:  # Recognize playing vs myself
    mode = "cooperate"
  elif opp_memory[:5] == ["cooperate","defect","cooperate","defect","defect"]: # Tit_for_tat recognition
    mode = "cooperate"

  # if len(opp_memory) >= 7: # Is a guard like this needed below?

  # Was an elif connected to the above block, fixed the bug, why would that be an issue?
  if mode == "cooperate" and (opp_memory[:7] == edge_case_1_1 or opp_memory[:7] == edge_case_1_2 or opp_memory[:7] == edge_case_1_3):
    mode = "defect"
  elif mode == "cooperate" and (opp_memory[:7] == edge_case_2_1 or opp_memory[:7] == edge_case_2_2 or opp_memory[:7] == edge_case_2_3):
    mode = "defect"
  
  if mode:
    return mode
  else: # Safety in case mode is not set somehow
    return "defect"

def tit_for_devil(player):
  opp_memory = player.get_opponent_memory()
  if len(opp_memory) == 0:  # Turn 1 defect
    return "defect"
  
  strat_choice = tit_for_tat(player)
  
  if len(opp_memory) == 49:   #Calculate opponent score
    my_memory = player.get_self_memory()
    opp_score = 0

    for i, opp_choice in enumerate(opp_memory): # Calculate opponent_score
      if my_memory[i] == "cooperate":
        if opp_choice == "cooperate":
          opp_score += 3
        else:
          opp_score += 5
      elif my_memory[i] == "defect":
        if opp_choice == "defect":
          opp_score += 1
        #else opp_score += 0 # Not needed if they cooperate
    
    if opp_score >= player.get_score():
      strat_choice = bad_guy(player)
   
  return strat_choice

def cool_beans(player):
  opp_memory = player.get_opponent_memory()
  my_memory = player.get_self_memory()

  if len(opp_memory) in [0, 1]:  # Turn 1 & 2 defect
    return "defect"
                                  #and opponent copied my last move
  if opp_memory[0] == "cooperate" and opp_memory[1] == my_memory[0]:
    return "cooperate"  # This will be "nice" to tit_for_tat (and random)
  else:
    return "defect"

def check_random(opponent_memory, self_memory):
  strategies = [good_guy, bad_guy, tit_for_tat, inverse_tit_for_tat]

  for strat in strategies:  # Go through every strat known
    temp = Player("temp", strat)
    if len(self_memory) > 0:  #guard against array out of bounds
      for i in range(len(self_memory)): # mini tournament for the strat
        choice1 = temp.get_choice()
        choice2 = self_memory[i]
        temp.add_choices(choice2, choice1)

      if temp.get_self_memory() == opponent_memory:
        return False

      temp.reset() 
  # If we make it here, we didn't match any strategies  
  return True 

def super_strat(player):
  opp_memory = player.get_opponent_memory()

  if len(opp_memory) <= 1:  # first 2 turns defect
    return "defect"
  elif len(opp_memory) == 2 and opp_memory[:2] == ["cooperate", "defect"]:  # Tft detector?
    player.set_temp_strat(good_guy)
  elif opp_memory[:2] in [["defect", "defect"], ["defect", "cooperate"], ["cooperate","cooperate"]] and len(opp_memory) == 2:
    player.set_temp_strat(bad_guy)

  if len(opp_memory) % 10 == 0: #every 10 turns
    if check_random(opp_memory, player.get_self_memory()):  # if opponent is random
      player.set_temp_strat(tit_for_tat)  # switch to tit_for_tat

  return player.get_temp_strat_result()

def name_here(player):
  opp_memory = player.get_opponent_memory()
  if len(opp_memory) > 2: # Added this guard here
    if opp_memory[:3] == ["cooperate", "defect", "defect"]: # detect myself
      return "cooperate"
    elif opp_memory[:3] == ["cooperate", "cooperate", "defect"]:  # detect tft
      return "cooperate"
  elif len(opp_memory) == 0:  # Turn 1 defect
    return "cooperate"
  
  return "defect" # default when nothing else returns cooperate

#Add players here when adding them to the tournament 
def get_players(number_of_turns):
  players = []
  players.append(Player('50/50', random_or_preset_choices, Player.get_chance_array(50, number_of_turns)))
  players.append(Player('Mr.Moore', good_guy))
  players.append(Player('devil', bad_guy))
  players.append(Player('tit_for_tat', tit_for_tat))
  players.append(Player('inverse_tft', inverse_tit_for_tat))
  players.append(Player('hoi4', heart_of_iron_4))
  players.append(Player('name_here', random_or_preset_choices, Player.get_choice_pattern_array( [1, 1, 0, 1, 1, 1, 0, 1, 1, 1] ,number_of_turns)))
  players.append(Player('Bob', random_or_preset_choices, Player.get_choice_pattern_array([1, 0, 1, 1, 1, 1, 0, 1, 1, 1], number_of_turns)))
  players.append(Player('A^2', tit_for_devil))
  players.append(Player('kaynes', random_or_preset_choices, Player.get_chance_array(75 ,number_of_turns)))
  players.append(Player('Jeff', bad_guy))
  players.append(Player('Cool_beans', cool_beans))
  players.append(Player('DaSupaStrat', super_strat))
  players.append(Player('name_here', name_here))
  return players
  



def main():
  ROUND_LENGTH = 10
  fifty_fifty = Player('50/50', random_or_preset_choices, Player.get_chance_array(50, ROUND_LENGTH))
  name_here = Player('name_here', random_or_preset_choices)
  fifty_fifty.print_all()
  print("###############\n")
  name_here.print_all()
  print("###############\nChoices:\n")
  print("50/50", fifty_fifty.get_choice())
  print("hoi4", name_here.get_choice())
  print("###############\n")
  fifty_fifty.print_all()
  print("###############\n")
  name_here.print_all()

if __name__ == "__main__":
  main()