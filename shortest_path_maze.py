# -*- coding: utf-8 -*-
"""shortest_path_maze.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EUXGvQMVn456xXKcRFkUH8yNB9qJEe8c
"""

import numpy as np

environment_rows= 11
environment_columns = 11

q_values = np.zeros((environment_rows, environment_columns, 4))

actions = ['up', 'right', 'left', 'right']



rewards = np.full((environment_rows,environment_columns),-100)
rewards[0,5] = 100
aisles = {}
aisles = {} 
aisles[1] = [i for i in range(1, 10)]
aisles[2] = [1, 7, 9]
aisles[3] = [i for i in range(1, 8)]
aisles[3].append(9)
aisles[4] = [3, 7]
aisles[5] = [i for i in range(11)]
aisles[6] = [5]
aisles[7] = [i for i in range(1, 10)]
aisles[8] = [3, 7]
aisles[9] = [i for i in range(11)]

for row_index in range(1,10):
  for column_index in aisles[row_index]:
    rewards[row_index, column_index] = -1

for row in rewards:
  print(row)

def is_terminal_state(cri, cci):
  if rewards[cri, cci] == -1:
    return False
  else:
    return True


def get_starting_location():
  cri = np.random.randint(environment_rows)
  cci = np.random.randint(environment_columns)
  while is_terminal_state(cri, cci):
    cri = np.random.randint(environment_rows)
    cci = np.random.randint(environment_columns)
  return cri,  cci

def get_next_action(cri, cci, epsilon):
  if np.random.random() < epsilon:
    return np.argmax(q_values[cri, cci])
  else:
    return np.random.randint(4)

def get_next_location(cri, cci, action_index):
  new_row_index = cri
  new_column_index = cci
  if actions[action_index] == 'up' and cri > 0:
    new_row_index -= 1
  elif actions[action_index] == 'right' and cci < environment_columns - 1:
    new_column_index += 1
  elif actions[action_index] == 'down' and cri < environment_rows - 1:
    new_row_index += 1
  elif actions[action_index] == 'left' and cci> 0:
    new_column_index -= 1
  return new_row_index, new_column_index

def get_shortest_path(start_row_index, start_column_index):
  if is_terminal_state(start_row_index, start_column_index):
    return[]
  else:
    current_row_index, current_column_index = start_row_index, start_column_index
    shortest_path = []
    shortest_path.append([current_row_index, current_column_index])
    #continue moving along the path until we reach the goal (i.e., the item packaging location)
    while not is_terminal_state(current_row_index, current_column_index):
      #get the best action to take
      action_index = get_next_action(current_row_index, current_column_index, 1.)
      #move to the next location on the path, and add the new location to the list
      current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
      shortest_path.append([current_row_index, current_column_index])
    return shortest_path

epsilon = 0.9
discount_factor = 0.9
learning_rate = 0.9

for episode in range(1000):
  r, c = get_starting_location()

  while not is_terminal_state(r,c):
    action_index = get_next_action(r,c,epsilon)
    oldr, oldc = r, c
    r, c = get_next_location(r, c, action_index)

    reward = rewards[r, c]
    oldq = q_values[oldr, oldc, action_index]
    temporal_difference = reward + (discount_factor * np.max(q_values[r, c])) - oldq
    new_q_value = oldq + (learning_rate * temporal_difference)
    q_values[oldr, oldc, action_index] = new_q_value

print('Training complete!')

print(q_values)

print(get_shortest_path(3, 9)) #starting at row 3, column 9
print(get_shortest_path(5, 0)) #starting at row 5, column 0
print(get_shortest_path(9, 5)) #starting at row 9, column 5
print(get_shortest_path(1,2))