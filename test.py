from inputimeout import inputimeout, TimeoutOccurred

def stockton():
  for _ in range(10):
    try:
      # Give the user 5 seconds to type "close door"
      action = inputimeout(prompt="Quick! Type 'close door' to defend: ", timeout=5)
    
      if action.strip().lower() == 'close door':
        print("You closed the door in time!")
      else:
        print("That didn't do anything!")
        
    except TimeoutOccurred:
      print("\n*BZZT!* You ran out of time! The animatronic got inside.")