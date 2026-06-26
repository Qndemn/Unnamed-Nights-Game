import random
import time
import sys
from inputimeout import inputimeout, TimeoutOccurred
import math

inputs = ["1", "2", "3"]
power = 100
auxPower = 100
flashPower = 100
door1 = False
door2 = False
night = 0
effective_speed = 1.5
stocktonDistance = 20
checkersDistance = 25
bishopDistance = 15
checkerSides = ["left", "right"]
checkerSide = random.choice(checkerSides)
timeLeft = 50
charge = False
phoneActive = False
callType = None

def phoneCall():
   global phoneActive, callType, stocktonDistance, checkersDistance
   if power > 3:
      choice = input("Phone Call:\n1. Commercials (Stockton speeds up but once eliminated starts farther away)\n2. Static (Stockton is paused)\n3. Turn Off Phone\nChoose (number): ")
      if choice in["1", "2"]:
         phoneActive = True
      if choice == "1":
         callType = "commercials"
      elif choice == "2":
         callType = "static"
      elif choice == "3":
         callType = None
         phoneActive = False
      else:
         print("!! INVALID CHOICE !!")

def flashlight():
   global flashPower, bishopDistance
   if flashPower >= 25:
      flashPower -= 25
      choice = input("Check:\n1. Front\n2. Left\n3. Right\n\nChoose (number): ")
      if choice == "1":
         bishopDistance += 3
         if bishopDistance > 20:
            bishopDistance = 20
         print("\n<< FLASH >>")
         time.sleep(0.25)
         print(f"\nThe Bishop is {bishopDistance} away.")
      elif choice == "2":
         if checkerSide == "left":
            print(f"Checkers is {checkersDistance} away.")
            time.sleep(0.75)
         else:
            print("Nothing there.")
      elif choice == "3":
         if checkerSide == "right":
            print(f"Checkers is {checkersDistance} away.")
            time.sleep(0.75)
         else:
            print("Nothing there.")
   else:
      print("!! OUT OF FLASHLIGHT POWER !!")
   time.sleep(1.5)
def stockton():
  global power, auxPower, door1, door2
  stockton_speed = max(effective_speed - (night * 0.15), 0.5)
  print("\n"*40)
  print("SELL! SELL! SELL!")
  time.sleep(1)
  for _ in range(10):
    chosenInput = random.choice(inputs)
    try:
      action = inputimeout(prompt=f"BLOCK '{chosenInput}': ", timeout=stockton_speed)
    
      if action.strip().lower() == chosenInput:
        print("<click>")
        print("\n"*40)
      else:
        print("><>< ZZZT ><><")
        if power > 0:
           power -= 50
           if power < 0:
              power = 0
        else:
           auxPower -= 50
           if auxPower < 0:
              auxPower = 0
        door1 = True
        door2 = True
        
        break
    except TimeoutOccurred:
      print("\n><>< ZZZT ><><")
      if power > 0:
        power -= 50
        if power < 0:
          power = 0
      else:
        auxPower -= 50
        if auxPower < 0:
          auxPower = 0
      door1 = True
      door2 = True
  print("\nStockton Scurries Away...")
  time.sleep(0.75)

def intro():
   global night
   print("Welcome to Unnamed Nights Game!")
   print("This game is meant to be a testing place as well as its own game.")
   print("Please point out any errors or bugs, and I hope you enjoy the nights and bossfight!")
   choice = input("\n(enter to continue) ")
   if choice == "1":
     night = 1
   elif choice == "2":
     night = 2
   elif choice == "3":
     night = 3
   elif choice == "4":
     night = 4
   elif choice == "5":
     night = 5

def main_game():
    global door1, door2, power, auxPower, flashPower, checkerSide, checkersDistance, bishopDistance, stocktonDistance, charge, night, timeLeft, callType, phoneActive
    if power > 0:
       power -= 2
       if power < 0:
          power = 0
    elif auxPower > 0:
       auxPower -= 2
       if auxPower < 0:
          auxPower = 0
    if power > 0 and door1:
       power -= 4
       if power < 0:
          power = 0
    elif auxPower > 0 and door1:
       auxPower -= 4
       if auxPower < 0:
          auxPower = 0
    if power > 0 and door2:
       power -= 4
       if power < 0:
          power = 0
    elif auxPower > 0 and door2:
       auxPower -= 4
       if auxPower < 0:
          auxPower = 0
    if phoneActive and power > 3:
       power -= 3
    elif phoneActive and auxPower > 3:
       auxPower -= 3
    if charge:
       charge = False
       if power > 0:
          power += 2
       elif auxPower > 0:
          auxPower += 2
    if power == 0 and auxPower == 0:
       print("\n"*40)
       print("!!! BLACKOUT !!!")
       time.sleep(0.5)
       print("\nYou Died.")
       time.sleep(0.5)
       input("(enter to continue :D)")
       timeLeft = 0
       night -= 1
       return
    if checkersDistance <= 0:
       if checkerSide == "left" and door1:
          print("\nCheckers bangs on the left door...")
          time.sleep(0.5)
          print("BANG")
          time.sleep(0.25)
          print("BANG")
          time.sleep(0.25)
          print("BANG")
          time.sleep(0.75)
          print("... and retreats back into the darkness.")
          checkersDistance = int(max(5, 25 - night * 1.5))
          checkerSide = random.choice(checkerSides)
          time.sleep(1)
       elif checkerSide == "right" and door2:
          print("\nCheckers bangs on the right door...")
          time.sleep(0.5)
          print("BANG")
          time.sleep(0.25)
          print("BANG")
          time.sleep(0.25)
          print("BANG")
          time.sleep(0.75)
          print("... and retreats back into the darkness.")
          checkersDistance = int(max(5, 25 - night * 1.5))
          checkerSide = random.choice(checkerSides)
          time.sleep(1)
       else:
          print("\n"*40)
          print("T I M E ' S  U P ,  B U C K O !")
          time.sleep(0.75)
          print("\n\n-=== CHECKERS GOT IN ===-")
          print("To avoid Checkers, check to see which side he's on, and when he approaches, close the respective door.")
          print("You died.")
          input("\n(enter to continue :D)")
          timeLeft = 0
          night -= 1
          return
    if checkersDistance > 0:
       if checkersDistance > night and night > 1:
         checkersDistance = checkersDistance - math.ceil((night / 2))
       else:
         checkersDistance -= 1
    if bishopDistance <= 0:
       print("\n"*40)
       print("K̸̨̨̧̛̛̺̻̲̬͙̗̜͚̞͔̱̼̟̥̞̮̳̝̞͚̱̳̪̲̫͉̠̥̤̪͇̗͚̺̦̜͛́̂͒̉̉͋̃́̔͗̀̏̂̌̓̉̿̄́̀̐́͒͌̌̋͗͒͌͑͛̂͒̆͑́̉̍͊̈́̽̋́̈́̅̽̽̍͑͌́͛͒͂͊̎̎̈́̂̇̌̎̀͛̉̀̅̏̈̉͗͌̑̋̆̀͒̑̍͂͆̈́̆̉̓͂̾̄̄͒̒̈̃́͑̏̅̀̀̂̋͂̌̂̇̈́͑̐̀̈́̏̀̈́̆͂̆͊́͋͆͋̐̋͑̀͆̄̇͆͒̔̓̈́́̎͂̐͆͗̃̒́͗̀͌̀̇̿͐̂͆̂̆́̿̓́̇͆̆̃̐̓́̐̽̈́͆͊̓́̀̀̉̆͗́̑̾́̎́̈́̐͌́̓̊͆̂͒͂̿̀́̄͂̈̾̊̈́̔̎̔̒̈́͂̃̋̆̃̽̾̉̽͆̂̾̏̍̀̌̓̏͊̓̉̀́̑̈̏͗́̓́̽̆̀͆̓̏̐̓͛̏̅͌͗͑̄̄͒͆̾̅͘͘͘̚̚͘̕̕͘̕̕̕̕͜͝͝͠͝͝͝͠͝͝͠͠͝͝͝͝͠͠͝͝͝͠͝͠F̴̨̡̢̡̛̛̙̰͚͉̬̥̤̟̝̱̖͔͕̠͚̣̼̟̭̠̘͇͖͇̣͔͙̗̺͕̟̰̗͖͙̦̱̼̣̭͉͙͉̬͙͕͖͉̩̥̫͕̻̭̥̹̬̩̺͗̀͋͆͑̑͂̂̃͊͑̊͗̄̈́͒̅̓̌̉̓͑͂̎͌̊̍̈́̈͒̀̆͋͗͌̓̈̈́͑̃̓͛̑̓̇̐̓̔́̔͂́́̑̔̐͊͊̀́͐̾̀̀͗͒̾́̈́͐̐̈̅̋͌̈́̈̔̌́͛̐̈̋̈́̌̍̎̿̽̋̀̀̌̀̉͐̓͐͊̆̅͊̂͂̂͛̊͐̊̉̈̈́͋̄̌̉̒́̈́̐̆͐̓͊́̀͛͐͛͐̽̋̄͐̋̽̈̽̍̏̽̑̀̓̏͂̾́͘̕̚͘̕̚̚̕͜͜͜͜͜͝͠͠͠͝͝͝͝͝͝ͅS̷̢̧̢̨̨̢̨̡̢̨̢̨̨̡̛̛̛̛̛̛̘̦̻̣̭͓̜̺̪̫̳̫̜̖̼͙̹͍̤̬̱͍̮̙̭̳̺̗͔̰̺̳̣̹̗͕̞̱̙̤͍̱̤̭̟̗̻̳̫̞̪͔̬͕̝̫̻̫̹͈̤̻̬͕̝͇͉͚͇̱͍̟̫̭̱̰̖̞̘̰̺͓͉͓̪̖̭͇̮̖͕͙͙̪̲̱͖̜͎̝̫̯̥͍̟͙͈̘̖̼͚͇̜̫̞͍̣̟̩͔̩͉̳͚̳̯͖͓̬̳̻͙̲̤̟̝͉͙̭̣͙̰̻̬͎͖̜͍͚̻͖̰̝͖̣̖͚̹͚̟̯̮͊̀̎̐̑̉͗͂̌͆͂̑͊͊̀͆̓̓̔̓̀͗͆͗̈́̓̆́́̀̌͑͌̀̓̑̃̏̂̈́̏͋͒̈͗̀̋̉̔́̃̃͊̔̅̋̅̉̈́͊͒̀̊̊͂̍̀͑̂͂̍̑̊̎͋̀̄́̋͗̊͊͒̈͒̏͂̄̾̐̆̇̾͆̀̽̈̄̂̔̅̋̀́̐̅́̏̆͐̋͋͊́̽̃̈́̍̍̉̊̀̏̏͌̊͐̎̏̒̂͌̎́̐̓̓̽͊́̈̋̿̊̽̐̃̈̈̒̈́̅̍̈́́̄́̆̃̊͊͑̈́̔̉̑̒̀͆̽̈̋́̍͊͂͂̈́͂̒͑̿̌́̈́̒̓͒̓̑̈́̀͊̉̆̈̉̅̌͛̄̋̉̎̽̌̋̚͘̕̚̕̚̕̚̕͘̕̕̕̕͘͘̕̚̕̚͜͜͜͜͜͜͜͜͜͜͝͝͝͠͝͠͠͝͝͠͝͝͝͝͠͠ͅͅH̸̡̡̡̡̧̨̡͎̱͚̘̲̳͖̟̪͍͍͓̦͙̟̟̠͕͍̺̭̤̬͇̱͙̖̱̘̰͎̞̰̣̦͚͍͖͍̗̻͚̩̘̲̦͉̦̟͚̗̬̱̫̦͎̦̗̄͑͜͜͜ͅĄ̵̢̨̨̢̛̛̛̖͖̣͙̖̭̦͓̞̹̳̲̺͎̤̜͔͓͉̼͙̦̹̬͈̼̣̥̟̩͎͕͚̠̮̹̩͖̟̰̯̘͍̯̤͖̼̮̝̣͙̩͙̯̳̤̪̗͍̦̮͚͉̼̱̗͕̪̬̟͇̯̆͒͌̎̈͑͐̃̋̽̇́̃́͊̊͐̿̅̏̓̇͂̍̌̍̒͑̈́͋̐̂͂͌̉͆̊̓͗͗̐́̈̆̑̽̿͒̐̃̇̆̊͆͋͋̌͗͆̔̽̂̓̽́̒͂͑͊̊̄͌͆͊́̎̽̐̀̂̏̀̓̓̽̈́͒̈́̄͌͊͐͆̆̽͐͑̍̋́̆͊̆͌̉̊͗̑̑̑̓̍͗͊͗͆̓̈̔̄͘̚̚̕͘̕̕̚̕͝͝͝͝͠͝͠͝͠͝͠͝ͅͅĶ̴̡̨̡̢̡̡̧̧̨̢̢̢̨̡̧̡̹̖̞̖̝̳̬͙̗̗͎͈̤̩̝̲͓͍͈͔̰̭̣̹̹̯̹͙̩̥͖̱͎͈̱̖̦͎̳̮̰̼̦̞̯̝̝̲͎̣̲̙̘͓͕̮̝̘̫̫̥͔̮͕̭̳̥̦̞̯͍̰͓̭̲̪͚̪͍̭̹̦̞̹̳̟̹̭̗͎̬̝͉̩̜̖̲͈̯̥̺̮̬̳̯̭̣̩̃̎̽͗̓́̄̇̐̌̇̽̾̔͋̏̉̇̓͜͜͜͝͠͠͠͝ͅͅͅŞ̶̢̡̡̡̡̢̢̧̟̭͍͇̥̟͓̯̼̫̣̟̝̪͓̟̯̟̭͍̥̜̻̤̰̘̜̺͕̞͉̗͍̻̭̪̝̩̪̞̲̖̲̖̜̪̩̙͈̩̹͇̪̣͓̦̬̭͕͖̘͚̘͈̯̟̰̦̳̹͓̝̣̰̜̮̰͎̘̤͕͈̳̟̘͔̲̳̝͍̖̦̘͓̜̖̹̖͕̱͚̠̩͖̺̞̦͎̞̩͍͚̫̮͔͎̜̙̰̘̝͍͚̼̉̐͐͗̌̎͂͆̈͑̃̓̓͛̈̃́̃̔͑́̓̀͗͒̑̈́̉̃͊̒͒͂̓̽̋̈̽̑̃̀́͑͒̓͌͑̊̾̏̇̿͊̈́́̀́͘͘̚͘͠͝͝͝͝ͅͅͅͅJ̷̨̡̡̧̨̢̲̣͎̩̳͕̻̣̤̠̠̻̘̟̻̭̬̯̳͕͕̹̭͙̫̰͚̦̙̭̭̗̪͇̮̱̘̫̩̻͉͉̳̳̳̤͓͉̞̳̭͕̼̳͈̦͍̲͓̹̜̫̹̜̞͓͕͎̥͕̮͂͐͂̐̏͆͜͜͠D̷̨̡̡̨̧̧̨̡̨̧̨̨̧̡̢̨̡̧̢̧̧̧̨̧̛̜͉̩̤̬̫̖͖̞̭̯̰͖̻̩̣̣͍͖̰̦̫̭̙͍͎̗̱̰͈̻̬̟̩̥̗̰̭̲̻̹̞̱͚͖̝̹̤͔̼̫͓͎͈̝̪͕̭̮̤̺͈̻͖̣̦̱̩̖̘͉̞͈̠̰͎͕̞̟̝̙̲̬͈̙͚̤̻̩̗̣̘̻͓̪͍̠͕͉̫̻̺͓̘̪͈̪̼̭̼͍̦̜͓̜̲̻̠̜̰̘̙͇̟͔͓̦͉̰̳̖̠̟̪̜̩̦̮͚͖̰̟̻͔̘͇̲̗̪̖̭̫̱͉͈̳̻̲̫̞̪͕̲̰̯̮̣̥̼̩̳̤͙̻̪̯̭̥̖͇̪̠̘̹͚̗͚̫̰̜͉͕͎͎̹̪̖̯̥̘̣̬̜̟̻̩̯͕̤̥̜̻̼͚̪̫͈̙͕̱͔̫̣̦̜̜̹̻̖̖̎̓̎͂̓̽̀͊̈́̑̎́̈́͒̄̒̋̏̄̏̽̈̂͑̒̃͐̃͗̐̍̎͋͂̓̔̀̑̄̏̔̈́̎̓̇̋͒̓̅͂̉̑̄͆͐̂̈͒̆̔͋̾̈̈́̿̀͑͋̕͘̚͜͜͜͜͝͝͠͠ͅͅͅͅͅͅͅͅͅH̵̢̧̢̡̨̨̧̧̧̢̡̡̢̡̢̢̨̨̢̢̧̡̨̨̨̧̨̧̢̛̗͍̙̝̱͇̻̯̺̣̬͍̰̘̺̱̱̙̣͎̟͉̰̻͍̝̰͔͕̳̼̞̠̲̩̫̤̙̖̫̠͎͓͍̘̙̼̟̰͖̝̜̬̮̦͙̘̤̻͎̥̫͙̗̥̼̝͈̞̤̗͈̝͖͇̲̥̬̳̩͙̹͇̤̤̫̺̠̤͓̤͙̳̳͓̰͇̥̼̺͕̞̜̤̮̯̖̭̫̠̲̗̰̳̦̩̻̩̬̤̳̟̭̞̻̗̦̫͚̪̪̝͇̦̘̤̭̟̣̰̫̭̪̹̤̪͉̟̘͎̞͇̮̖͓̭͖̬̖͔̰̖̪̥̪͓͚̞͙͖͎͈̼̦̰͚͔̮͓̦̣̺̘̱̳̘͖̣͕̰͎̥͉̘̱̤̜̫̜̺̟̱̠̘̺̟̩͖͉̠̺̺͙̥̩̩̝̥͍̳̫͙͉̯̺̱̘̤̝͔͈͕̩̬̰̥̘̪͙̣͇͐̌͗̈́́̀͒͐̈́͂̾̈́̃̌̀̋̓̀̈́̈́̈͑͗̄͒̎̑͌̾̏̐͒͒͑̒̍̑̉̓͑̈́̅͂̐̓͗̈́̽̐͐͊͘̕̚̚͜͜͝͝͝͠͠ͅͅͅͅͅͅͅJ̴̨̧̧̨̢̢̧̡̧̧̧̢̨̨̢̨̢̛̛̛̛̺̩͔͖͔̦̤̻̝̠͓͕̲̠̬͚̩͖͈͉̫̫͎͙͕̺̯͉̦̫̻̰͉̲̼͕̖̖͖̠͔̟̳͉̩̗̱̘̪̟͈̣̠̪̤̯͚̫̝̺͔͔̜͕̱̩̪̗̻̫͉̹͕̫̘̪̮̥̰̹̞̝̤̭̫͇͈̘̞̫̬̬̰̙̼̠̱̤̙̱̗̳̗̹̠̝͎̜̪̬̘̮̥̳̰̦͈̦͙͔̙̹̹̩̤͍͉͉͔͉̺̲̰̠̭̳͚͍͖͕͓͇̟͎̖͙̞̙̼͙̺̰̻̤̗̰̙͍̜̬̞̺͍̥̱͍̰͇̬̠̫̻̜̖̙͉̰̻̙̭̟̭͓̤̱̻̗͇̪̮̙̦̬̪͙̲̮̜̗̟̗̠̪̮̖̼̭̦̣̹̥̫̪̱̫̟̣̋̃̓̂̓̿͋͗͋͆̋̐̈́̿́̅̉̀̇̾̇̽̋̿͌̔͑́́͆͌̔̏̇͑́͑̾̎̊͛̃͑̿̀̌̉͌̾́̽̈͐̂̒̽͑̿̈́̋͗͐́́̀́͑́͒̍̈́́̑̍̏̏̏̈̾̇̀̓̒͛̍́̐̈́̄̌̈́̅̀̾̓̐͑͒͋͗͋͆̇̿̔̊̇̏̎́̒̎̀͆̌̃̎̆͒̏̇̍͑̋͋̌̃͆̒̃̉͒̔̽̍̃̒̋̃̉̊̀͋̑̒̏̑̓̄̃̐̈́̐́̂͐̽̋̓͗̍̇͌̉̏̀̑͐̀̓́̀͊̈́̑̃͂͊̿̉̈́̂̍͆̑̈́̔͊̽̂̚͘͘̕͘̚̕̚̚͘̚͘̕̚̚̕̚̚͜͜͜͜͜͜͠͝͠͝͝͝͝͠͠͠͝͝͝ͅͅK̸̡̨̡̢̨̧̡̧̢̡̡̨̡̢̧̨̛̗̭̣͈̤͉͍̖̳̣̪͈̩̠͓̭͙͎̞̫̼͉̥̟̙̗͇̯͔̙̣̞̜͎̰̠̝̹͎͈͓͈̩̜̫̝̞͍͔͔̻̪̙̪̻̫̰̠͎̮̹̬͔̺̱͙̞̗̯̪͔̠͎̠̱̮̳̤͖̰͓̦̤͍̹̹̺̝͓̠͙̻̤̠͙͙̙̪̥̞͔̪̰͓̲͔̩͔̻̲̱͈̭̟̺̬̙̦̱̤̟̬̼̜͕͎͙͓̖̙͎̪̝͍͕̞̥̲͖͇̥̟̣͚̣̙͇͎̘͔̩̥̼̭̠̜̙̞̫͈̥̋́̍̒̊͋͛̂͐̎́̈́̈̂̅̈́̊͂̂̾̿͒̓̃͒̿̅͐̇̈̋̅͑̅͋̓̎̔͌̐͋͆̽̈́́̽̈́̊̀̐͛̿̌͆́̒̓̚̚͜͜͜͜͜͠͝͝͝ͅͅF̵̨̡̢̡̧̨̢̨̡̧̨̧̢̧̡̡̢̨̡̧̡̨̢̢̡̧̡̛̛̛̛̛͉͙̜͖̥̣̘̪͈̟̬͕̥̭̳͚̥̤̰͎̰̠̘͙̱̪̫͕̮̼͍̦̭̼̖͈̜̣̳͙̰͇̙̺̱̦͈͇̤̳̬͕͇̱͍̰̱͙̤̣̣̫͍͇̦̮̺͎̪̝̗̰͍̮̦̙͈̦͔͙͓͇̼̱͓̼͔̼̲̤̪̤̫͎̜͓̖̤͍̜̻̩̝̬̯̗̖̙̟̳͉̣̝͔̜̖͈͎͓̝͉̳͇̮͉̤̱̪̳̠͔̲͇̦̰̞͖̗̫͙̥̙̣̞͓̞̝͕̜̥̼̖̭̜͕̮̰͍̳͓̣̪͈͙̜̖͇͔̼̫͍̟͖̖͎͙͕̼̮̯̦̱̣̲͇̞̣̞̱̭̱̪̼͍͇͙̭̗̟̦̝̬̩͙̬͍̠̬͎͔͎͕̟̮̗̤͖̱̦̣̹̙͚͍̮̥͓̗͚̯̞̅̓̆̔̽̉̿̅͗̈̊̆̐͒̋͊͋͊̿̏̅̄͆͆̄͆͐̆̅͗̆́̋̀͊͒̋̆̌͛̊̆̈́̃̏̓̈́̿̓̍͑͛̈͒̈́̉̓̆̈́̒̈́͆̄́͑͛̆̾̕͘̚̚͜͜͜͜͠͝͠ͅͅH̵̨̡̨̡̡̨̢̧̡̛̛̛̫̺̭̭͙̖̲̜͖͕̭̞̦̬̻̗̳̣̫̹̞̖̮̩̦̳̬̱͔̗̖̭̣̲̖̙̲̬̭̟̱̻̰̹͇̯̜̣̞̼̱͔̰͍̯̝̞̗͕͖̪̖͚͚͍̳̤͈͕̯̫̩͙͕̪̪͖̝̞̗̱͇̠̖̮͉̟͙̙̞̣̻̯͍̱̺̩̺̖͕̥͙̻̠̙̗̯̯̖͓̻̣͙̝͇̠̑́̿̇̈́͐̿̾̅̏̍̈̃̒̐̈́̈̈͌͛͒̌̀͒̋̈́̽̈́̋͒͑͆̌͌̐̓̐̈́̐̒̅̎̌͂̀̈́̍̽̊͗̈̋̐̈́̃̉̆̈́̋͗̓̔̿̈́́̋̒́͐̉̑̈́͑̅͑̅̀̊͆͋͗̓̀̚͘͘͘̚͜͜͜͝͠͠͝͝ͅ")
       time.sleep(0.75)
       print("\n\n-=== THE BISHOP GOT IN ===-")
       print("To avoid The Bishop, regularly flash him in the front hallway.")
       print("\nYou died.")
       input("\n(enter to continue :D)")
       timeLeft = 0
       night -= 1
       return
    elif bishopDistance > 0:
       bishopDistance -= 1
    if stocktonDistance <= 0:
       stockton()
       stocktonDistance = int(max(5, 20 - night * 1.5))
       if callType == "commercials":
          stocktonDistance += 15
    elif stocktonDistance > 0 and callType != "static":
       stocktonDistance -= night
       if timeLeft >= 5 and timeLeft <= 10:
          stocktonDistance -= 1
       if callType == "commercials":
          stocktonDistance -= 5
    print("\n"*40)
    print(f"TIME LEFT: {timeLeft}\n")
    print("-=========== OFFICE ===========-")
    print(f"Power: {power}")
    print(f"Auxiliary Power: {auxPower}")
    print(f"Flashlight Power: {flashPower}")
    print(f"Phone: {phoneActive} ({callType})")
    print(f"Door 1: {door1} - Door 2: {door2}")
    print("\nOptions:\n1. Flashlight (then choose side)\n2. Open/Close Left\n3. Open/Close Right\n4. Charge Flashlight\n5. Charge Power (Aux can only be paused)\n6. Phone Call (then choose type)")
    choice = input("Choose (number): ")
    if choice == "1":
       flashlight()
    elif choice == "2":
       #I'll add conditionals later
       if door1:
          door1 = False
       else:
          door1 = True
    elif choice == "3":
       if door2:
          door2 = False
       else:
          door2 = True
    elif choice == "4":
       flashPower = min(flashPower + random.randint(15, 30), 100)
       print("-) bweeeeee (-")
       time.sleep(1.5)
    elif choice == "5" and not door1 and not door2 and not phoneActive:
       if power > 0:
          power = min(power + random.randint(5, 15), 100)
       else:
          print("!!! POWER IS OUT, AUX CAN ONLY BE PAUSED !!!")
       print("<>< bweeeee ><>")
       charge = True
       time.sleep(1.5)
    elif choice == "5" and (door1 or door2 or phoneActive):
       print("!!! CANNOT CHARGE WHILE DOOR IS OPEN OR PHONE IS ACTIVE !!!")
       time.sleep(1)
    elif choice == "6":
       phoneCall()
    else:
       print("!!! INVALID INPUT !!!")
       time.sleep(1)

intro()

while True:
   night += 1
   timeLeft = 50
   power = 100
   flashPower = 100
   auxPower = 100
   door1 = False
   door2 = False
   stocktonDistance = int(max(5, 20 - night * 1.5))
   checkersDistance = int(max(5, 25 - night * 1.5))
   bishopDistance = int(max(6, 15 - night * 1.5))
   checkerSide = random.choice(checkerSides)
   phoneActive = False
   callType = None
   print(f"-==== Night {night} ====-")
   startnight = night
   time.sleep(2)
   while timeLeft > 0:
      timeLeft -= 1
      main_game()
   if timeLeft == 0 and night == startnight:
      print("\n"*40)
      print("!!! 6 AM !!!")
      time.sleep(1.5)
   else:
      continue