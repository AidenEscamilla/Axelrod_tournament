import numpy as np
import random
import time

class Player:
  def __init__(self, name, strategy, chance_array=None, num_rounds=None):
    self.opponent_memory = []
    self.self_memory = []
    self.name = name
    self.total_score = 0
    self.strategy = strategy
    self.chance_array = chance_array
    self.chance_iter = 0
    self.temp_strat = None
    self.opponent_score = 0
    self.total_num_rounds = num_rounds  # This is cheating, the argument should be deleted as well as this variable
    # Including the number of rounds is to appease the tricky_tft strat group when I pull the rug out
    # And say "What if we didn't do just 100 rounds"

  def __str__(self):
    return f"{self.name} scored: {self.total_score}"
  
  def print_all(self):
    print(f"name: {self.name}\nscore: {self.total_score}\nopp_memory: {self.opponent_memory}\nself_memory: {self.self_memory}\nstrategy: {self.strategy}\nchance_array: {self.chance_array}\nchance_iter: {self.chance_iter}")

  def reset_memory(self):
    self.opponent_memory = []
    self.self_memory = []

  def reset_iterator(self):
    self.chance_iter = 0

  def reset_temp_strat(self):
    self.temp_strat = None

  def reset_opponent_score(self):
    self.opponent_score = 0

  def reset(self):
    self.reset_memory()
    self.reset_iterator()
    self.reset_temp_strat()
    self.reset_opponent_score()

  def iterate_chance(self):
    self.chance_iter += 1

  
  def add_choices(self, opponents_choice, self_choice):
    self.opponent_memory.append(opponents_choice)
    self.self_memory.append(self_choice)
    if opponents_choice == "cooperate":
      if self_choice == "cooperate":
        self.add_score(3) # nice & nice = +3 points
        self.add_opponent_score(3)
      else:
        self.add_score(5) # nice & betrayed them = +5 points
        self.add_opponent_score(0)
    else:
      if self_choice == "cooperate":
        self.add_score(0) # defect & nice (was betrayed) = +0 points
        self.add_opponent_score(5)
      else:
        self.add_score(1) # defect & defect = +1 points
        self.add_opponent_score(1)
  
  def get_opponent_memory(self):
    return self.opponent_memory
  
  def get_self_memory(self):
    return self.self_memory
  
  def add_score(self, points):
    self.total_score += points

  def add_opponent_score(self, points):
    self.opponent_score += points
  
  def get_score(self):
    return self.total_score
  
  def get_opponent_score(self):
    return self.opponent_score
  
  def get_choice(self):
    return self.strategy(self)
  
  def set_temp_strat(self, strat_to_remember):
    self.temp_strat = strat_to_remember

  def get_opponent_number_of_defects(self):
    count = 0
    for choice in self.opponent_memory:
      if choice == "defect":
        count += 1
    
    return count
  
  def get_opponent_number_of_cooperates(self):
    count = 0
    for choice in self.opponent_memory:
      if choice == "cooperate":
        count += 1
    
    return count

  def get_temp_strat_result(self):
    if self.temp_strat == None:
      return None
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

    return output_array.tolist()
  
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
# Class 1 strats

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

def random_or_preset_choices(player): # 50%/ 50%
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

def recognize(player):
  opp_memory = player.get_opponent_memory()
  if len(opp_memory) > 2: # Added this guard here
    if opp_memory[:3] == ["cooperate", "defect", "defect"]: # detect myself
      return "cooperate"
    elif opp_memory[:3] == ["cooperate", "cooperate", "defect"]:  # detect tft
      return "cooperate"
  elif len(opp_memory) == 0:  # Turn 1 be nice
    return "cooperate"
  
  return "defect" # default when nothing else returns cooperate

def computer_goose(player):
  opp_memory = player.get_opponent_memory()
  my_memory = player.get_self_memory()

  if len(opp_memory) in [0, 1]: # first 2 rounds
    return "defect"
  
  if opp_memory[:2] == ["cooperate", "cooperate"]:
    if len(opp_memory) == 3 and opp_memory[2] == "defect":
      return "defect"
    else:
      player.set_temp_strat(bad_guy)
  elif opp_memory[:2] == ["defect", "defect"]:
    if len(opp_memory) == 3 and opp_memory[2] == "cooperate":
      return "defect"
    else:
      player.set_temp_strat(bad_guy)
  elif opp_memory[:2] == ["cooperate", "defect"]:
    if len(opp_memory) == 3 and opp_memory[2] == "cooperate":
      return "defect"
    elif len(opp_memory) < 3:
      player.set_temp_strat(bad_guy)
      return "cooperate"
  elif opp_memory[:2] == ["defect", "cooperate"]:
    if len(opp_memory) == 3 and opp_memory[2] == "defect":
      return "defect"
    else:
      return "defect"
    
  #if count_cooperates(opp_memory) > 50 or count_defects(opp_memory) > 50
  if len(my_memory) > 5:
    if my_memory[-6:] == opp_memory[-6:]:
      return "cooperate"
    
  if player.get_temp_strat_result() == None:
    return "defect"
  else:
    return player.get_temp_strat_result()

# Class 2 strats
def semi_random(player):
  opp_memory = player.get_opponent_memory()
  round_number = len(opp_memory)
  choice_for_the_round = round_number % 7

  # Get random choice
  random.seed(time.time())
  random_choice = random.randint(0,1)
  if random_choice: # 1 == defect
    random_choice = "defect"
  else: # 0 == cooperate
    random_choice = "cooperate"

  match choice_for_the_round:
    case 0:
      return random_choice
    case 1:
      return random_choice
    case 2:
      # Get opposite of opponent last did
      opposite_of_opponent = opp_memory[-1]

      if opposite_of_opponent == "defect":  # If they last defected
        opposite_of_opponent = "cooperate"  # Swap to cooperate
      else:                                 # Else, they must've cooperated last time
        opposite_of_opponent = "defect"     # Swap to defect
      
      return opposite_of_opponent
    case 3:
      return opp_memory[-1] # Do what enemy last did 
    case 4:
      return opp_memory[-1] # Do what enemy last did 
    case 5:
      return random_choice
    case 6:
      # Get opposite of opponent last did
      opposite_of_opponent = opp_memory[-1]

      if opposite_of_opponent == "defect":  # If they last defected
        opposite_of_opponent = "cooperate"  # Swap to cooperate
      else:                                 # Else, they must've cooperated last time
        opposite_of_opponent = "defect"     # Swap to defect
      
      return opposite_of_opponent

def be_nice_twice(player):
  opp_memory = player.get_opponent_memory()
  myself_memory = player.get_self_memory()

  if len(opp_memory) == 0:  # Turn 1 be mean
    return "defect"
  
  if (player.get_score() - player.get_opponent_score()) >= 7: # If we are winning by 7 or more
    return "defect" # Ignore everything and defect
  else:
    if opp_memory[-1] == "defect":  # if they were mean, be mean back
      return "defect"
    elif opp_memory[-1] == "cooperate" and (myself_memory[-2:] != ["cooperate", "cooperate"]):  # if they were nice, be nice for a max of 2 turns
      return "cooperate"
    else: # if i've been nice for 2 turns
      return "defect"

def semi_random_2(player):
  opp_memory = player.get_opponent_memory()
  round_number = len(opp_memory)
  choice_for_the_round = round_number % 9

  # Get random choice
  random.seed(time.time())
  random_choice = random.randint(0,1)
  if random_choice: # 1 == defect
    random_choice = "defect"
  else: # 0 == cooperate
    random_choice = "cooperate"

  match choice_for_the_round:
    case 0:
      return "defect"
    case 1:
      return "defect"
    case 2:
      return random_choice
    case 3:
      return opp_memory[-1] # Do what enemy last did 
    case 4:
      # Get opposite of opponent last did
      opposite_of_opponent = opp_memory[-1]

      if opposite_of_opponent == "defect":  # If they last defected
        opposite_of_opponent = "cooperate"  # Swap to cooperate
      else:                                 # Else, they must've cooperated last time
        opposite_of_opponent = "defect"     # Swap to defect
      
      return opposite_of_opponent
    case 5:
      return "defect"
    case 6:
      # Do the opponents first move
      return opp_memory[0]
    case 7:
      return random_choice
    case 8:
      defects = player.get_opponent_number_of_defects()
      cooperates = player.get_opponent_number_of_cooperates()
      if defects > cooperates:
        return "cooperate"
      else: # Else coops > defects
        return "defect"

def two_chances(player):
  opp_memory = player.get_opponent_memory()
  myself_memory = player.get_self_memory()

  if len(opp_memory) == 0:  # on turn 1
    return "cooperate"      # be nice
  

  if player.get_opponent_number_of_defects() == 1:  # If they're mean once
    return "cooperate"  # Give them a chance
  elif player.get_opponent_number_of_defects() == 2 and myself_memory[-1] == "cooperate": 
    # if they're mean twice and I gave them a chance
    player.set_temp_strat(tit_for_tat)

  temp_strat = player.get_temp_strat_result()
  if temp_strat:  # If there is no temp_strat, this will fail/be false
    return temp_strat
  else:
    return "cooperate"
    
def grass_touchers(player):
  return tit_for_tat(player)

# Class 3

def dominators(player):
  self_memory = player.get_self_memory()
    # player.chance_iter == 4 if it's been 4 rounds
    # (len(self_mem) // 4) % 3 = every 4 rounds we switch
  if player.chance_iter == 4 and (len(self_memory) // 4) % 3 == 0:
    player.reset_iterator()
    player.set_chance_array(Player.get_chance_array(80, 4)) # switch to 80% defect
  elif player.chance_iter == 4 and (len(self_memory) // 4) % 3 == 1:
    player.reset_iterator()
    player.set_chance_array(Player.get_choice_pattern_array([1,1,0,0], 4))  # switch to 50% defect
  elif player.chance_iter == 4 and (len(self_memory) // 4) % 3 == 2:
    player.reset_iterator()
    player.set_chance_array(Player.get_chance_array(100, 4))  # switch to 100% defect
  


  bool_choice = player.get_next_array_element() # Get the choice
  if bool_choice: # 1 == defect
    return "defect"
  else: # 0 == cooperate
    return "cooperate" 

def meaner_tft(player):
  opponent_memory = player.get_opponent_memory()

  # For round 1 or round 2
  if len(opponent_memory) == 0 or len(opponent_memory) == 1:
    return "defect"
  
  return opponent_memory[-1] # Copy what they did last turn

def mean_tft(player):
  opponent_memory = player.get_opponent_memory()

  # For round 1 or round 2
  if len(opponent_memory) == 0:
    return "defect"
  else:
    return opponent_memory[-1] # Copy what they did last turn

def swap_random(player):
  self_memory = player.get_self_memory()
    # player.chance_iter == 5 if it's been 5 rounds
    # (len(self_mem) // 5) % 5 = every 5 rounds we switch strats
  if player.chance_iter == 5 and (len(self_memory) // 5) % 5 == 0:
    player.reset_iterator()
    player.set_chance_array(Player.get_chance_array(40, 5)) # switch to 40% defect
  elif player.chance_iter == 5 and (len(self_memory) // 5) % 5 == 1:
    player.reset_iterator()
    player.set_chance_array(Player.get_chance_array(100, 5))  # switch to 100% defect
  elif player.chance_iter == 5 and (len(self_memory) // 5) % 5 == 2:
    player.reset_iterator()
    player.set_chance_array(Player.get_chance_array(70, 5))  # switch to 70% defect
  elif player.chance_iter == 5 and (len(self_memory) // 5) % 5 == 3:
    player.reset_iterator()
    player.set_chance_array(Player.get_chance_array(20, 5))  # switch to 20% defect
  elif player.chance_iter == 5 and (len(self_memory) // 5) % 5 == 4:
    player.reset_iterator()
    player.set_chance_array(Player.get_chance_array(65, 5))  # switch to 65% defect
  


  bool_choice = player.get_next_array_element() # Get the choice
  if bool_choice: # 1 == defect
    return "defect"
  else: # 0 == cooperate
    return "cooperate" 

def special_case(player):
  opponent_memory = player.get_opponent_memory()
  if len(opponent_memory) <= 92:  # For the first 92 turns
    return "defect"
  
  if len(opponent_memory) >= 93: # On turn 93 and beyond
    opp_choice_set = set(opponent_memory[-93:]) # Make a set of their last 93 choices

    # Set can ONLY equal = {"coop"} OR {"defect"} OR {"coop","defect"}

    # If they cooperated for the last 93 rounds    
    if len(opp_choice_set) == 1 and (opp_choice_set.pop() == "cooperate"):
      return "cooperate"  # be nice
    else:
      return "defect" # be mean

def tricky_tft(player):
  opponent_memory = player.get_opponent_memory()

  if len(opponent_memory) == 0: # On turn 1
    return "cooperate"  # be nice
  elif len(opponent_memory) == (player.total_num_rounds - 1): # the last turn
    return "defect" # be mean
  else: # All other turns
    return opponent_memory[-1] 
  # Do what the opponent did last round

def pattern_recognition(player):
  opponent_memory = player.get_opponent_memory()

  # On turn 1 or 3
  if len(opponent_memory) == 0 or len(opponent_memory) == 2:
    return "defect"
  elif len(opponent_memory) == 1: # On turn 2
    return "cooperate"
  
  opponent_pattern = opponent_memory[0:3] # Get their first 3 moves
  pattern_recognized = None

  if opponent_pattern == ["cooperate", "defect", "cooperate"]:
    pattern_recognized = "tit_for_tat"
  elif opponent_pattern == ["defect", "defect", "defect"]:
    pattern_recognized = "devil"
  elif opponent_pattern == ["defect", "cooperate", "defect"]:
    pattern_recognized = "self" # and inverse_tft
  elif opponent_pattern == ["cooperate","cooperate","cooperate"]:
    pattern_recognized = "Mr.Moore"

  if pattern_recognized == "Mr.Moore":
    player.set_temp_strat(bad_guy)
  elif pattern_recognized == "devil" or pattern_recognized == "tit_for_tat":
    player.set_temp_strat(tit_for_tat)
  elif pattern_recognized == "self": # Or inverse_tft
    player.set_temp_strat(inverse_tit_for_tat)
  else:
    player.set_temp_strat(tit_for_tat)

  return player.get_temp_strat_result()


#Add players here when adding them to the tournament 
def get_players(number_of_turns, class_name):
  players = []

  # Bots
  bot_players = [
    Player('50/50', random_or_preset_choices, Player.get_chance_array(50, number_of_turns)),
    Player('Mr.Moore', good_guy),
    Player('inverse_tft', inverse_tit_for_tat),
    Player('tit_for_tat', tit_for_tat),
    Player('devil', bad_guy),
  ]

  # Class 1
  saffron_players = [
    Player('Name_here1', recognize),
    Player('DaSupaStrat', super_strat),
    Player('hoi4', heart_of_iron_4),
    Player('Name_here2', random_or_preset_choices, Player.get_choice_pattern_array( [1, 1, 0, 1, 1, 1, 0, 1, 1, 1] ,number_of_turns)),
    Player('Bob', random_or_preset_choices, Player.get_choice_pattern_array([1, 0, 1, 1, 1, 1, 0, 1, 1, 1], number_of_turns)),
    Player('A^2', tit_for_devil),
    Player('kaynes', random_or_preset_choices, Player.get_chance_array(75 ,number_of_turns)),
    Player('Jeff', bad_guy),
    Player('Cool_beans', cool_beans),
    Player('DaSupaStrat', super_strat),
    Player('Computer Goose', computer_goose)
  ]

  # Class 2
  cerulean_players = [
    Player('a_a', semi_random),
    Player('demo_dolphin', be_nice_twice),
    Player('team_Elo', random_or_preset_choices, Player.get_choice_pattern_array([1, 1, 1, 1, 0, 1, 1, 0], number_of_turns)),
    Player('glass_saturn', semi_random_2),
    Player('vroom', random_or_preset_choices, Player.get_choice_pattern_array([1, 1, 1, 1, 1, 0], number_of_turns)),
    Player('carlson_method', two_chances),
    Player('wipers', random_or_preset_choices, Player.get_chance_array(40 ,number_of_turns)),
    Player('grass_touchers', grass_touchers),
    Player('pickles', random_or_preset_choices, Player.get_choice_pattern_array([0,1,1,0,0,1,1,0,1,1],number_of_turns))
  ]

  # Class 3
  lilac_players = [
    Player('dominators', dominators, Player.get_chance_array(80,4)),
    Player('serpent', meaner_tft),
    Player("Aztec_em", swap_random, Player.get_chance_array(40,5)),
    Player('Gold_qs', mean_tft),
    Player('name_here', bad_guy),
    Player('Lemon', random_or_preset_choices, Player.get_chance_array(70, number_of_turns)),
    Player('op_code', special_case),
    Player('pg13', tricky_tft, None, number_of_turns),
    Player('we_rock_inc.', random_or_preset_choices, Player.get_chance_array(70, number_of_turns)),
    Player('bananas', pattern_recognition)
  ]

  players += bot_players # Add the bots
  if class_name == "saffron": # Class 1
    players += saffron_players
  elif class_name == "cerulean": # Class 2
    players += cerulean_players
  elif class_name == "lilac": # Class 3
    players += lilac_players
  else: # All classes
    players += saffron_players
    players += cerulean_players
    players += lilac_players

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