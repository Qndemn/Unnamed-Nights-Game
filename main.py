import random
import time
import sys
from inputimeout import inputimeout, TimeoutOccurred

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

def flashlight():
   global flashPower, bishopDistance
   if flashPower > 0:
      flashPower -= 25
      choice = input("Check:\n1. Front\n2. Left\n3. Right\n\nChoose (number): ")
      if choice == "1":
         bishopDistance += 3
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
  stockton_speed = max(effective_speed - (night * 0.15), 0.35)
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
           power -= 15
           if power < 0:
              power = 0
        else:
           auxPower -= 15
           if auxPower < 0:
              auxPower = 0
        door1 = True
        door2 = True
        
        break
    except TimeoutOccurred:
      print("\n><>< ZZZT ><><")
      if power > 0:
        power -= 15
        if power < 0:
          power = 0
      else:
        auxPower -= 15
        if auxPower < 0:
          auxPower = 0
      door1 = True
      door2 = True
  print("\nStockton Scurries Away...")
  time.sleep(0.75)

def intro():
    print("Welcome to Unnamed Nights Game!")
    print("This game is meant to be a testing place as well as its own game.")
    print("Please point out any errors or bugs, and I hope you enjoy the nights and bossfight!")
    input("\n(enter to continue) ")

def main_game():
    global door1, door2, power, auxPower, flashPower, checkerSide, checkersDistance, bishopDistance, stocktonDistance, charge
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
       sys.exit()
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
          checkersDistance = 25 - night * 2
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
          checkersDistance = 25 - night * 2
          checkerSide = random.choice(checkerSides)
          time.sleep(1)
       else:
          print("\n"*40)
          print("T I M E ' S  U P ,  B U C K O !")
          time.sleep(0.75)
          print("\n\n-=== CHECKERS GOT IN ===-")
          print("To avoid Checkers, check to see which side he's on, and when he approaches, close the respective door.")
          print("You died.")
          input("\n(enter to continue/crash the game bc im too lazy to add a restart :D)")
          sys.exit()
    if checkersDistance > 0:
       checkersDistance -= 1
    if bishopDistance <= 0:
       print("\n"*40)
       print("K̸̨̨̧̛̛̺̻̲̬͙̗̜͚̞͔̱̼̟̥̞̮̳̝̞͚̱̳̪̲̫͉̠̥̤̪͇̗͚̺̦̜͛́̂͒̉̉͋̃́̔͗̀̏̂̌̓̉̿̄́̀̐́͒͌̌̋͗͒͌͑͛̂͒̆͑́̉̍͊̈́̽̋́̈́̅̽̽̍͑͌́͛͒͂͊̎̎̈́̂̇̌̎̀͛̉̀̅̏̈̉͗͌̑̋̆̀͒̑̍͂͆̈́̆̉̓͂̾̄̄͒̒̈̃́͑̏̅̀̀̂̋͂̌̂̇̈́͑̐̀̈́̏̀̈́̆͂̆͊́͋͆͋̐̋͑̀͆̄̇͆͒̔̓̈́́̎͂̐͆͗̃̒́͗̀͌̀̇̿͐̂͆̂̆́̿̓́̇͆̆̃̐̓́̐̽̈́͆͊̓́̀̀̉̆͗́̑̾́̎́̈́̐͌́̓̊͆̂͒͂̿̀́̄͂̈̾̊̈́̔̎̔̒̈́͂̃̋̆̃̽̾̉̽͆̂̾̏̍̀̌̓̏͊̓̉̀́̑̈̏͗́̓́̽̆̀͆̓̏̐̓͛̏̅͌͗͑̄̄͒͆̾̅͘͘͘̚̚͘̕̕͘̕̕̕̕͜͝͝͠͝͝͝͠͝͝͠͠͝͝͝͝͠͠͝͝͝͠͝͠F̴̨̡̢̡̛̛̙̰͚͉̬̥̤̟̝̱̖͔͕̠͚̣̼̟̭̠̘͇͖͇̣͔͙̗̺͕̟̰̗͖͙̦̱̼̣̭͉͙͉̬͙͕͖͉̩̥̫͕̻̭̥̹̬̩̺͗̀͋͆͑̑͂̂̃͊͑̊͗̄̈́͒̅̓̌̉̓͑͂̎͌̊̍̈́̈͒̀̆͋͗͌̓̈̈́͑̃̓͛̑̓̇̐̓̔́̔͂́́̑̔̐͊͊̀́͐̾̀̀͗͒̾́̈́͐̐̈̅̋͌̈́̈̔̌́͛̐̈̋̈́̌̍̎̿̽̋̀̀̌̀̉͐̓͐͊̆̅͊̂͂̂͛̊͐̊̉̈̈́͋̄̌̉̒́̈́̐̆͐̓͊́̀͛͐͛͐̽̋̄͐̋̽̈̽̍̏̽̑̀̓̏͂̾́͘̕̚͘̕̚̚̕͜͜͜͜͜͝͠͠͠͝͝͝͝͝͝ͅS̷̢̧̢̨̨̢̨̡̢̨̢̨̨̡̛̛̛̛̛̛̘̦̻̣̭͓̜̺̪̫̳̫̜̖̼͙̹͍̤̬̱͍̮̙̭̳̺̗͔̰̺̳̣̹̗͕̞̱̙̤͍̱̤̭̟̗̻̳̫̞̪͔̬͕̝̫̻̫̹͈̤̻̬͕̝͇͉͚͇̱͍̟̫̭̱̰̖̞̘̰̺͓͉͓̪̖̭͇̮̖͕͙͙̪̲̱͖̜͎̝̫̯̥͍̟͙͈̘̖̼͚͇̜̫̞͍̣̟̩͔̩͉̳͚̳̯͖͓̬̳̻͙̲̤̟̝͉͙̭̣͙̰̻̬͎͖̜͍͚̻͖̰̝͖̣̖͚̹͚̟̯̮͊̀̎̐̑̉͗͂̌͆͂̑͊͊̀͆̓̓̔̓̀͗͆͗̈́̓̆́́̀̌͑͌̀̓̑̃̏̂̈́̏͋͒̈͗̀̋̉̔́̃̃͊̔̅̋̅̉̈́͊͒̀̊̊͂̍̀͑̂͂̍̑̊̎͋̀̄́̋͗̊͊͒̈͒̏͂̄̾̐̆̇̾͆̀̽̈̄̂̔̅̋̀́̐̅́̏̆͐̋͋͊́̽̃̈́̍̍̉̊̀̏̏͌̊͐̎̏̒̂͌̎́̐̓̓̽͊́̈̋̿̊̽̐̃̈̈̒̈́̅̍̈́́̄́̆̃̊͊͑̈́̔̉̑̒̀͆̽̈̋́̍͊͂͂̈́͂̒͑̿̌́̈́̒̓͒̓̑̈́̀͊̉̆̈̉̅̌͛̄̋̉̎̽̌̋̚͘̕̚̕̚̕̚̕͘̕̕̕̕͘͘̕̚̕̚͜͜͜͜͜͜͜͜͜͜͝͝͝͠͝͠͠͝͝͠͝͝͝͝͠͠ͅͅH̸̡̡̡̡̧̨̡͎̱͚̘̲̳͖̟̪͍͍͓̦͙̟̟̠͕͍̺̭̤̬͇̱͙̖̱̘̰͎̞̰̣̦͚͍͖͍̗̻͚̩̘̲̦͉̦̟͚̗̬̱̫̦͎̦̗̄͑͜͜͜ͅĄ̵̢̨̨̢̛̛̛̖͖̣͙̖̭̦͓̞̹̳̲̺͎̤̜͔͓͉̼͙̦̹̬͈̼̣̥̟̩͎͕͚̠̮̹̩͖̟̰̯̘͍̯̤͖̼̮̝̣͙̩͙̯̳̤̪̗͍̦̮͚͉̼̱̗͕̪̬̟͇̯̆͒͌̎̈͑͐̃̋̽̇́̃́͊̊͐̿̅̏̓̇͂̍̌̍̒͑̈́͋̐̂͂͌̉͆̊̓͗͗̐́̈̆̑̽̿͒̐̃̇̆̊͆͋͋̌͗͆̔̽̂̓̽́̒͂͑͊̊̄͌͆͊́̎̽̐̀̂̏̀̓̓̽̈́͒̈́̄͌͊͐͆̆̽͐͑̍̋́̆͊̆͌̉̊͗̑̑̑̓̍͗͊͗͆̓̈̔̄͘̚̚̕͘̕̕̚̕͝͝͝͝͠͝͠͝͠͝͠͝ͅͅĶ̴̡̨̡̢̡̡̧̧̨̢̢̢̨̡̧̡̹̖̞̖̝̳̬͙̗̗͎͈̤̩̝̲͓͍͈͔̰̭̣̹̹̯̹͙̩̥͖̱͎͈̱̖̦͎̳̮̰̼̦̞̯̝̝̲͎̣̲̙̘͓͕̮̝̘̫̫̥͔̮͕̭̳̥̦̞̯͍̰͓̭̲̪͚̪͍̭̹̦̞̹̳̟̹̭̗͎̬̝͉̩̜̖̲͈̯̥̺̮̬̳̯̭̣̩̃̎̽͗̓́̄̇̐̌̇̽̾̔͋̏̉̇̓͜͜͜͝͠͠͠͝ͅͅͅŞ̶̢̡̡̡̡̢̢̧̟̭͍͇̥̟͓̯̼̫̣̟̝̪͓̟̯̟̭͍̥̜̻̤̰̘̜̺͕̞͉̗͍̻̭̪̝̩̪̞̲̖̲̖̜̪̩̙͈̩̹͇̪̣͓̦̬̭͕͖̘͚̘͈̯̟̰̦̳̹͓̝̣̰̜̮̰͎̘̤͕͈̳̟̘͔̲̳̝͍̖̦̘͓̜̖̹̖͕̱͚̠̩͖̺̞̦͎̞̩͍͚̫̮͔͎̜̙̰̘̝͍͚̼̉̐͐͗̌̎͂͆̈͑̃̓̓͛̈̃́̃̔͑́̓̀͗͒̑̈́̉̃͊̒͒͂̓̽̋̈̽̑̃̀́͑͒̓͌͑̊̾̏̇̿͊̈́́̀́͘͘̚͘͠͝͝͝͝ͅͅͅͅJ̷̨̡̡̧̨̢̲̣͎̩̳͕̻̣̤̠̠̻̘̟̻̭̬̯̳͕͕̹̭͙̫̰͚̦̙̭̭̗̪͇̮̱̘̫̩̻͉͉̳̳̳̤͓͉̞̳̭͕̼̳͈̦͍̲͓̹̜̫̹̜̞͓͕͎̥͕̮͂͐͂̐̏͆͜͜͠D̷̨̡̡̨̧̧̨̡̨̧̨̨̧̡̢̨̡̧̢̧̧̧̨̧̛̜͉̩̤̬̫̖͖̞̭̯̰͖̻̩̣̣͍͖̰̦̫̭̙͍͎̗̱̰͈̻̬̟̩̥̗̰̭̲̻̹̞̱͚͖̝̹̤͔̼̫͓͎͈̝̪͕̭̮̤̺͈̻͖̣̦̱̩̖̘͉̞͈̠̰͎͕̞̟̝̙̲̬͈̙͚̤̻̩̗̣̘̻͓̪͍̠͕͉̫̻̺͓̘̪͈̪̼̭̼͍̦̜͓̜̲̻̠̜̰̘̙͇̟͔͓̦͉̰̳̖̠̟̪̜̩̦̮͚͖̰̟̻͔̘͇̲̗̪̖̭̫̱͉͈̳̻̲̫̞̪͕̲̰̯̮̣̥̼̩̳̤͙̻̪̯̭̥̖͇̪̠̘̹͚̗͚̫̰̜͉͕͎͎̹̪̖̯̥̘̣̬̜̟̻̩̯͕̤̥̜̻̼͚̪̫͈̙͕̱͔̫̣̦̜̜̹̻̖̖̎̓̎͂̓̽̀͊̈́̑̎́̈́͒̄̒̋̏̄̏̽̈̂͑̒̃͐̃͗̐̍̎͋͂̓̔̀̑̄̏̔̈́̎̓̇̋͒̓̅͂̉̑̄͆͐̂̈͒̆̔͋̾̈̈́̿̀͑͋̕͘̚͜͜͜͜͝͝͠͠ͅͅͅͅͅͅͅͅͅH̵̢̧̢̡̨̨̧̧̧̢̡̡̢̡̢̢̨̨̢̢̧̡̨̨̨̧̨̧̢̛̗͍̙̝̱͇̻̯̺̣̬͍̰̘̺̱̱̙̣͎̟͉̰̻͍̝̰͔͕̳̼̞̠̲̩̫̤̙̖̫̠͎͓͍̘̙̼̟̰͖̝̜̬̮̦͙̘̤̻͎̥̫͙̗̥̼̝͈̞̤̗͈̝͖͇̲̥̬̳̩͙̹͇̤̤̫̺̠̤͓̤͙̳̳͓̰͇̥̼̺͕̞̜̤̮̯̖̭̫̠̲̗̰̳̦̩̻̩̬̤̳̟̭̞̻̗̦̫͚̪̪̝͇̦̘̤̭̟̣̰̫̭̪̹̤̪͉̟̘͎̞͇̮̖͓̭͖̬̖͔̰̖̪̥̪͓͚̞͙͖͎͈̼̦̰͚͔̮͓̦̣̺̘̱̳̘͖̣͕̰͎̥͉̘̱̤̜̫̜̺̟̱̠̘̺̟̩͖͉̠̺̺͙̥̩̩̝̥͍̳̫͙͉̯̺̱̘̤̝͔͈͕̩̬̰̥̘̪͙̣͇͐̌͗̈́́̀͒͐̈́͂̾̈́̃̌̀̋̓̀̈́̈́̈͑͗̄͒̎̑͌̾̏̐͒͒͑̒̍̑̉̓͑̈́̅͂̐̓͗̈́̽̐͐͊͘̕̚̚͜͜͝͝͝͠͠ͅͅͅͅͅͅͅJ̴̨̧̧̨̢̢̧̡̧̧̧̢̨̨̢̨̢̛̛̛̛̺̩͔͖͔̦̤̻̝̠͓͕̲̠̬͚̩͖͈͉̫̫͎͙͕̺̯͉̦̫̻̰͉̲̼͕̖̖͖̠͔̟̳͉̩̗̱̘̪̟͈̣̠̪̤̯͚̫̝̺͔͔̜͕̱̩̪̗̻̫͉̹͕̫̘̪̮̥̰̹̞̝̤̭̫͇͈̘̞̫̬̬̰̙̼̠̱̤̙̱̗̳̗̹̠̝͎̜̪̬̘̮̥̳̰̦͈̦͙͔̙̹̹̩̤͍͉͉͔͉̺̲̰̠̭̳͚͍͖͕͓͇̟͎̖͙̞̙̼͙̺̰̻̤̗̰̙͍̜̬̞̺͍̥̱͍̰͇̬̠̫̻̜̖̙͉̰̻̙̭̟̭͓̤̱̻̗͇̪̮̙̦̬̪͙̲̮̜̗̟̗̠̪̮̖̼̭̦̣̹̥̫̪̱̫̟̣̋̃̓̂̓̿͋͗͋͆̋̐̈́̿́̅̉̀̇̾̇̽̋̿͌̔͑́́͆͌̔̏̇͑́͑̾̎̊͛̃͑̿̀̌̉͌̾́̽̈͐̂̒̽͑̿̈́̋͗͐́́̀́͑́͒̍̈́́̑̍̏̏̏̈̾̇̀̓̒͛̍́̐̈́̄̌̈́̅̀̾̓̐͑͒͋͗͋͆̇̿̔̊̇̏̎́̒̎̀͆̌̃̎̆͒̏̇̍͑̋͋̌̃͆̒̃̉͒̔̽̍̃̒̋̃̉̊̀͋̑̒̏̑̓̄̃̐̈́̐́̂͐̽̋̓͗̍̇͌̉̏̀̑͐̀̓́̀͊̈́̑̃͂͊̿̉̈́̂̍͆̑̈́̔͊̽̂̚͘͘̕͘̚̕̚̚͘̚͘̕̚̚̕̚̚͜͜͜͜͜͜͠͝͠͝͝͝͝͠͠͠͝͝͝ͅͅK̸̡̨̡̢̨̧̡̧̢̡̡̨̡̢̧̨̛̗̭̣͈̤͉͍̖̳̣̪͈̩̠͓̭͙͎̞̫̼͉̥̟̙̗͇̯͔̙̣̞̜͎̰̠̝̹͎͈͓͈̩̜̫̝̞͍͔͔̻̪̙̪̻̫̰̠͎̮̹̬͔̺̱͙̞̗̯̪͔̠͎̠̱̮̳̤͖̰͓̦̤͍̹̹̺̝͓̠͙̻̤̠͙͙̙̪̥̞͔̪̰͓̲͔̩͔̻̲̱͈̭̟̺̬̙̦̱̤̟̬̼̜͕͎͙͓̖̙͎̪̝͍͕̞̥̲͖͇̥̟̣͚̣̙͇͎̘͔̩̥̼̭̠̜̙̞̫͈̥̋́̍̒̊͋͛̂͐̎́̈́̈̂̅̈́̊͂̂̾̿͒̓̃͒̿̅͐̇̈̋̅͑̅͋̓̎̔͌̐͋͆̽̈́́̽̈́̊̀̐͛̿̌͆́̒̓̚̚͜͜͜͜͜͠͝͝͝ͅͅF̵̨̡̢̡̧̨̢̨̡̧̨̧̢̧̡̡̢̨̡̧̡̨̢̢̡̧̡̛̛̛̛̛͉͙̜͖̥̣̘̪͈̟̬͕̥̭̳͚̥̤̰͎̰̠̘͙̱̪̫͕̮̼͍̦̭̼̖͈̜̣̳͙̰͇̙̺̱̦͈͇̤̳̬͕͇̱͍̰̱͙̤̣̣̫͍͇̦̮̺͎̪̝̗̰͍̮̦̙͈̦͔͙͓͇̼̱͓̼͔̼̲̤̪̤̫͎̜͓̖̤͍̜̻̩̝̬̯̗̖̙̟̳͉̣̝͔̜̖͈͎͓̝͉̳͇̮͉̤̱̪̳̠͔̲͇̦̰̞͖̗̫͙̥̙̣̞͓̞̝͕̜̥̼̖̭̜͕̮̰͍̳͓̣̪͈͙̜̖͇͔̼̫͍̟͖̖͎͙͕̼̮̯̦̱̣̲͇̞̣̞̱̭̱̪̼͍͇͙̭̗̟̦̝̬̩͙̬͍̠̬͎͔͎͕̟̮̗̤͖̱̦̣̹̙͚͍̮̥͓̗͚̯̞̅̓̆̔̽̉̿̅͗̈̊̆̐͒̋͊͋͊̿̏̅̄͆͆̄͆͐̆̅͗̆́̋̀͊͒̋̆̌͛̊̆̈́̃̏̓̈́̿̓̍͑͛̈͒̈́̉̓̆̈́̒̈́͆̄́͑͛̆̾̕͘̚̚͜͜͜͜͠͝͠ͅͅH̵̨̡̨̡̡̨̢̧̡̛̛̛̫̺̭̭͙̖̲̜͖͕̭̞̦̬̻̗̳̣̫̹̞̖̮̩̦̳̬̱͔̗̖̭̣̲̖̙̲̬̭̟̱̻̰̹͇̯̜̣̞̼̱͔̰͍̯̝̞̗͕͖̪̖͚͚͍̳̤͈͕̯̫̩͙͕̪̪͖̝̞̗̱͇̠̖̮͉̟͙̙̞̣̻̯͍̱̺̩̺̖͕̥͙̻̠̙̗̯̯̖͓̻̣͙̝͇̠̑́̿̇̈́͐̿̾̅̏̍̈̃̒̐̈́̈̈͌͛͒̌̀͒̋̈́̽̈́̋͒͑͆̌͌̐̓̐̈́̐̒̅̎̌͂̀̈́̍̽̊͗̈̋̐̈́̃̉̆̈́̋͗̓̔̿̈́́̋̒́͐̉̑̈́͑̅͑̅̀̊͆͋͗̓̀̚͘͘͘̚͜͜͜͝͠͠͝͝ͅ")
       time.sleep(0.75)
       print("\n\n-=== THE BISHOP GOT IN ===-")
       print("To avoid The Bishop, regularly flash him in the front hallway.")
       print("\nYou died.")
       input("\n(enter to continue/crash the game bc im too lazy to add a restart :D)")
       sys.exit()
    elif bishopDistance > 0:
       bishopDistance -= 1
    if stocktonDistance <= 0:
       stockton()
       stocktonDistance = 20 - night * 2
    elif stocktonDistance > 0:
       stocktonDistance -= 1
    print("\n"*40)
    print(f"TIME LEFT: {timeLeft}\n")
    print("-=========== OFFICE ===========-")
    print(f"Power: {power}")
    print(f"Auxiliary Power: {auxPower}")
    print(f"Flashlight Power: {flashPower}")
    print(f"Door 1: {door1} - Door 2: {door2}")
    print("\nOptions:\n1. Flashlight (then choose side)\n2. Open/Close Left\n3. Open/Close Right\n4. Charge Flashlight\n5. Charge Power (Auto switch to Aux on Panic Mode)")
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
    elif choice == "5":
       if power > 0:
          power = min(power + random.randint(5, 15), 100)
       else:
          auxPower = min(auxPower + random.randint(5, 15), 100)
       print("<>< bweeeee ><>")
       charge = True
       time.sleep(1.5)

intro()

while True:
   night += 1
   timeLeft = 50
   checkerSide = random.choice(checkerSides)
   print(f"-==== Night {night} ====-")
   while timeLeft > 0:
      timeLeft -= 1
      main_game()
   if night == 6:
      print("\nY O U  W I N ! ! !")
      time.sleep(1)
      input("\n\n(press enter to exit)")
      sys.exit()