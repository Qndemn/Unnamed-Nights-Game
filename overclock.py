import random
import time
import sys
from inputimeout import inputimeout, TimeoutOccurred
import math
import threading
import select
import tty
import termios
from jumpscare import main, clear_screen

inputs = ["1", "2", "3"]
power = 100
auxPower = 100
flashPower = 100
door1 = False
door2 = False
overclockHp = 100
charge = False
heat = False
blackout = False
voltage = 0
overclockDistance = 8
overclockFront = 10
overclockDoor = None
fusesOn = 10
fuse1 = True
fuse2 = True
fuse3 = True
fuse4 = True
fuse5 = True
fuse6 = True
fuse7 = True
fuse8 = True
fuse9 = True
fuse10 = True
burner = True
timeFrozen = False


def check_death():
    global power, auxPower
    return power <= 0 and auxPower <= 0

def try_activate_blackout():
    global blackout, voltage
    if random.random() < voltage:
        blackout = True
        voltage = 0.0
        return True

def disable_random_fuse():
    global fusesOn, fuse1, fuse2, fuse3, fuse4, fuse5, fuse6, fuse7, fuse8, fuse9, fuse10
    active_fuses = [name for name in ["fuse1", "fuse2", "fuse3", "fuse4", "fuse5", "fuse6", "fuse7", "fuse8", "fuse9", "fuse10"] if globals()[name]]
    if not active_fuses:
        return None
    fuse_name = random.choice(active_fuses)
    globals()[fuse_name] = False
    fusesOn = max(0, fusesOn - 1)
    return fuse_name


def breaker_box():
    global fuse1, fuse2, fuse3, fuse4, fuse5, fuse6, fuse7, fuse8, fuse9, fuse10, fusesOn
    fuseTurns = 0
    if fusesOn <= 3:
        fuseTurns = 3
    else:
        fuseTurns = 10 - fusesOn
    for _ in range(fuseTurns):
      print(f"Fuse 1: {'ON' if fuse1 else 'OFF'}")
      print(f"Fuse 2: {'ON' if fuse2 else 'OFF'}")
      print(f"Fuse 3: {'ON' if fuse3 else 'OFF'}")
      print(f"Fuse 4: {'ON' if fuse4 else 'OFF'}")
      print(f"Fuse 5: {'ON' if fuse5 else 'OFF'}")
      print(f"Fuse 6: {'ON' if fuse6 else 'OFF'}")
      print(f"Fuse 7: {'ON' if fuse7 else 'OFF'}")
      print(f"Fuse 8: {'ON' if fuse8 else 'OFF'}")
      print(f"Fuse 9: {'ON' if fuse9 else 'OFF'}")
      print(f"Fuse 10: {'ON' if fuse10 else 'OFF'}")
      fuseChosen = input("Choose a fuse to toggle (1-10): ")
      if fuseChosen == "1":
          fuse1 = not fuse1
          if fuse1:
              fusesOn += 1
          else:
              fusesOn -= 1
      elif fuseChosen == "2":
          fuse2 = not fuse2
          if fuse2:
              fusesOn += 1
          else:
              fusesOn -= 1
      elif fuseChosen == "3":
          fuse3 = not fuse3
          if fuse3:
              fusesOn += 1
          else:
              fusesOn -= 1
      elif fuseChosen == "4":
          fuse4 = not fuse4
          if fuse4:
              fusesOn += 1
          else:
              fusesOn -= 1
      elif fuseChosen == "5":
          fuse5 = not fuse5
          if fuse5:
              fusesOn += 1
          else:
              fusesOn -= 1
      elif fuseChosen == "6":
          fuse6 = not fuse6
          if fuse6:
              fusesOn += 1
          else:
              fusesOn -= 1
      elif fuseChosen == "7":
          fuse7 = not fuse7
          if fuse7:
              fusesOn += 1
          else:
              fusesOn -= 1
      elif fuseChosen == "8":
          fuse8 = not fuse8
          if fuse8:
              fusesOn += 1
          else:
              fusesOn -= 1
      elif fuseChosen == "9":
          fuse9 = not fuse9
          if fuse9:
              fusesOn += 1
          else:
              fusesOn -= 1
      elif fuseChosen == "10":
          fuse10 = not fuse10
          if fuse10:
              fusesOn += 1
          else:
              fusesOn -= 1

def flashlightV2():
    global flashPower, overclockFront
    if flashPower > 0:
        flashPower -= 25
        print(f"Overclock: {overclockFront}")
        print("(<<< FLASH >>>)")
        if overclockFront <= 3:
          print("Overclock's distance was reset.")
          overclockFront = -1
    else:
        print("!!! OUT OF FLASHLIGHT POWER !!!")
    time.sleep(1.5)

def burner_phone():
    global voltage
    if burner:
      mitchellsonLines = ["Hang in there.", "I'm on my way, pal.", "Keep fighting.", "Keep it hot.", "Weaken it.", "It can't last forever.", "We'll arrive shortly."]
      print(f"Mitchellson: ... {overclockDoor} Door... \n        ... {overclockDistance} away...")
      mitchellVoiceLine = random.choice(mitchellsonLines)
      print(mitchellVoiceLine)
      voltage = voltage + random.uniform(0.1, 0.25)
    else:
      print("## Nothing But Static ##")
    time.sleep(1.5)

def shortFuse():
    global blackout, power, auxPower, voltage
    duration_seconds = 20
    FUSE_COUNT = 5
    DRAIN_RATE = 0.02
    BOOST_AMOUNT = 0.25
    TICK_SPEED = 0.1

    fuses = [1.0] * FUSE_COUNT
    running = True
    time_left = 0
    time_up = False

    def drain_fuses():
        """Background fuse drain."""
        nonlocal running, fuses
        while running:
            for i in range(FUSE_COUNT):
                fuses[i] = max(0.0, fuses[i] - DRAIN_RATE)
            time.sleep(TICK_SPEED)

    def countdown_timer(seconds):
        """Ends the challenge after real-world time."""
        nonlocal running, time_up
        time.sleep(seconds)
        time_up = True
        running = False

    def print_fuses():
        print("\033[H\033[J", end="")  # clear screen
        print("=== SHORTFUSE (Real-Time) ===\n")
        print(time_left)
        for i, f in enumerate(fuses, start=1):
            bar = int(f * 20) * "█"
            print(f"Fuse {i}: {bar:<20} {int(f * 100)}%")
        print("\nType fuse number (1-5) to boost.")

    def get_nonblocking_input():
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            return sys.stdin.read(1)
        return None

    def shortfuse_minigame(duration_seconds):
        global blackout, power, auxPower, voltage, fuse1, fuse2, fuse3, fuse4, fuse5, fuse6, fuse7, fuse8, fuse9, fuse10, fusesOn
        nonlocal running, time_up, fuses, time_left

        start = time.time()
        print("!!! BLACKOUT !!!")
        print(f"ShortFuse Challenge Started ({duration_seconds} seconds)\n")

        # Start fuse drain
        drain_thread = threading.Thread(target=drain_fuses)
        drain_thread.daemon = True
        drain_thread.start()

        # Start real-time countdown
        timer_thread = threading.Thread(target=countdown_timer, args=(duration_seconds,))
        timer_thread.daemon = True
        timer_thread.start()

        # Nonblocking input setup
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)

        try:
            while True:
                time_left = round(duration_seconds - (time.time() - start), 1)
                print_fuses()

                # If time is up → break immediately
                if time_up:
                    break

                # Lose condition (before time ends)
                if any(f <= 0 for f in fuses):
                    running = False
                    print("\nFAILURE: A fuse burned out.")
                    time.sleep(1)
                    break

                # Player input
                key = get_nonblocking_input()
                if key and key.isdigit():
                    idx = int(key) - 1
                    if 0 <= idx < FUSE_COUNT:
                        fuses[idx] = min(1.0, fuses[idx] + BOOST_AMOUNT)

                time.sleep(0.05)

            # Time ended — check win/lose
            if not any(f <= 0 for f in fuses):
                print("\nSUCCESS: BLACKOUT FIXED!!!")
                blackout = False
                power = 75
                fuse1 = True
                fuse2 = True
                fuse3 = True
                fuse4 = True
                fuse5 = True
                fuse6 = True
                fuse7 = True
                fuse8 = True
                fuse9 = True
                fuse10 = True
                fusesOn = 10
                time.sleep(1)
            else:
                print("\nFAILURE: A fuse burned out.")
                time.sleep(1)

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            running = False

        print("\nShortFuse Challenge Ended.")

    shortfuse_minigame(duration_seconds)

def timeFreeze():
    if blackout:
        print("Ready?")
        input("(Enter to start minigame) ")
        shortFuse()
    else:
        print("!! NO BLACKOUT !!")
        time.sleep(1)

def stockFuse():
    global power, voltage, heat, blackout
    duration_seconds = 35
    FUSE_COUNT = 5

    # Fuses start at 25%
    fuses = [0.25] * FUSE_COUNT

    # Tuned drain + boost values
    DRAIN_RATE = 0.0025 / (overclockHp / 75)  # drain rate scales inversely with Overclock HP
    BOOST_AMOUNT = 0.3 * (overclockHp / 60)  # boost amount scales with Overclock HP
    TICK_SPEED = 0.035

    running = True
    time_left = duration_seconds
    start = False
    time_up = False
    start_time = None

    def drain_fuses():
        """Drain fuses smoothly while the challenge is active."""
        nonlocal running, fuses, start
        while running:
            for i in range(FUSE_COUNT):
                if start and fuses[i] > 0.0 and fuses[i] < 1.0:
                    fuses[i] = max(0.0, fuses[i] - DRAIN_RATE)
            time.sleep(TICK_SPEED)

    def countdown_timer(seconds):
        nonlocal running, time_up
        time.sleep(seconds)
        time_up = True
        running = False

    def print_fuses(prompt_idx):
        print("\033[H\033[J", end="")  # clear screen
        print("=== STOCKFUSE ===\n")
        print(f"Time Left: {time_left}s\n")
        for i, f in enumerate(fuses, start=1):
            bar = int(f * 20) * "█"
            tag = " <==" if i - 1 == prompt_idx else ""
            print(f"Fuse {i}: {bar:<20} {int(f * 100)}%{tag}")
        print("\nPress the fuse number to boost.")

    def get_key():
        """True ShortFuse-style no-enter input."""
        dr, _, _ = select.select([sys.stdin], [], [], 0)
        if dr:
            return sys.stdin.read(1)
        return None

    def choose_fuse_prompt():
        """Priority: lowest → mid → highest (excluding 100%)."""

        # Lowest: <25%
        low = [i for i, f in enumerate(fuses) if f < 0.25]
        if low:
            return random.choice(low)

        # Next: <35%
        mid = [i for i, f in enumerate(fuses) if f < 0.35]
        if mid:
            return random.choice(mid)

        # Highest fuse that is NOT maxed
        non_maxed = [i for i, f in enumerate(fuses) if f < 1.0]
        if non_maxed:
            return max(non_maxed, key=lambda i: fuses[i])

        # All maxed → choose any
        return random.randint(0, FUSE_COUNT - 1)

    def stockfuse_minigame(duration_seconds):
        global power, auxPower, voltage, heat, blackout
        nonlocal running, time_up, fuses, time_left, start, start_time

        print(f"Challenge Started ({duration_seconds} seconds)\n")

        # Enable raw input mode
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)

        current_prompt = choose_fuse_prompt()

        try:
            while running:
                if start_time is None:
                    time_left = duration_seconds
                else:
                    time_left = round(duration_seconds - (time.time() - start_time), 1)
                print_fuses(current_prompt)

                # WIN CONDITION: all fuses at 100%
                if all(f >= 1.0 for f in fuses):
                    running = False
                    print("\nSUCCESS: All fuses stabilized at 100%.")
                    heat = True
                    time.sleep(1)
                    return

                # TIME OUT = failure
                if time_up:
                    print("\nFAILURE: Time ran out.")
                    if power > 0:
                        power = min(power - 30, 0)
                    elif auxPower > 0:
                        auxPower = min(auxPower - 30, 0)
                    voltage += 0.2
                    time.sleep(1)
                    break

                # Burnout: ANY fuse hitting 0% = death
                if not time_up:
                  for f in fuses:
                    if f <= 0.0:
                      running = False
                      print("\nFAILURE: A fuse burned out.")
                      if power > 0:
                        power = max(power - 30, 0)
                      elif auxPower > 0:
                        auxPower = max(auxPower - 30, 0)
                      voltage += 0.2
                      time.sleep(1)
                      return

                # True ShortFuse input
                key = get_key()
                if key and key.isdigit():
                    idx = int(key) - 1

                    if not start:
                        start = True
                        start_time = time.time()
                        threading.Thread(target=drain_fuses, daemon=True).start()
                        threading.Thread(target=countdown_timer, args=(duration_seconds,), daemon=True).start()

                    if idx == current_prompt:
                        # Correct fuse hit
                        fuses[idx] = min(1.0, fuses[idx] + BOOST_AMOUNT)
                        current_prompt = choose_fuse_prompt()

                    else:
                        # Wrong fuse hit → penalty (only if not maxed)
                        if fuses[current_prompt] < 1.0:
                            fuses[current_prompt] = max(0.0, fuses[current_prompt] - (BOOST_AMOUNT / 2))

                time.sleep(TICK_SPEED)

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            running = False

        print("\nStockFuse Challenge Ended.")
        time.sleep(1)

    stockfuse_minigame(duration_seconds)

def overclock():
    global power, auxPower, flashPower, overclockDistance, overclockFront, overclockDoor, voltage, timeFrozen, heat, burner, fusesOn, fuse1, fuse2, fuse3, fuse4, fuse5, fuse6, fuse7, fuse8, fuse9, fuse10, charge, door1, door2, overclockHp, blackout
    print("\n"*40)
    print("Mitchellson: ... Overclock is awake ...\n      ... If you hold on, I can kill it...\n... this is it...\n              ... We'll get you out... \n... hang in there.")
    input("\n(Press Enter to continue) ")
    scale = max(1, int(overclockHp / 25))
    overclockDoor = random.choice(["Left", "Right"])
    overclockDistance = random.randint(5, scale + 5)
    burner = True
    while overclockHp > 0:
      time.sleep(2)
      scale = max(1, int(overclockHp / 25))
      if overclockDistance > 0:
        overclockDistance -= 1
      if overclockDistance <= 0:
        if overclockDoor == "Left":
            if door1:
                for _ in range(15):
                    time.sleep(0.05)
                    print("BANG")
                print("\n"*40)
            elif not door1:
                main()
                time.sleep(1)
                print("\n"*40)
                print("Overclock got in.")
                print("To avoid Overclock, you must shine the flashlight at it when it is in front of you.\nIf it is at a door, you must close the door to avoid it.")
                print("To damage Overclock, you must overheat the room. This will deal a chunk of damage on each use.")
                input("(Press Enter to restart :D) ")
                return
        elif overclockDoor == "Right":
            if door2:
                for _ in range(15):
                    time.sleep(0.05)
                    print("BANG")
                print("\n"*40)
            elif not door2:
                main()
                time.sleep(1)
                print("\n"*40)
                print("Overclock got in.")
                print("To avoid Overclock, you must shine the flashlight at it when it is in front of you.\nIf it is at a door, you must close the door to avoid it.")
                print("To damage Overclock, you must overheat the room. This will deal a chunk of damage on each use.")
                input("(Press Enter to restart :D) ")
                return
      if overclockDistance <= 0:
        overclockDoor = random.choice(["Left", "Right"])
        overclockDistance = random.randint(5, scale + 5)
        burner = True
        disable_random_fuse()
      if overclockFront == -1:
          overclockFront = random.randint(3, scale + 3)
      else:
          if overclockFront > 0:
              overclockFront -= 1
          elif overclockFront == 0:
                main()
                time.sleep(1)
                print("\n"*40)
                print("Overclock got in.")
                print("To avoid Overclock, you must shine the flashlight at it when it is in front of you.\nIf it is at a door, you must close the door to avoid it.")
                print("To damage Overclock, you must overheat the room. This will deal a chunk of damage on each use.")
                input("(Press Enter to restart :D) ")
                return
      if check_death():
          print("\n"*40)
          print("!!! ALL POWER DRAINED !!!")
          print("You died.")
          input("(Press Enter to restart :D) ")
          return
      fusesOn = sum([fuse1, fuse2, fuse3, fuse4, fuse5, fuse6, fuse7, fuse8, fuse9, fuse10])
      if power > 0:
        power -= 2 / max(1, fusesOn)
        if power < 0:
            power = 0
      elif auxPower > 0:
        auxPower -= (2 / max(1, fusesOn))
        if auxPower < 0:
          auxPower = 0
      if power > 0 and door1:
        power -= 4 / max(1, fusesOn)
        if power < 0:
          power = 0
      elif auxPower > 0 and door1:
        auxPower -= 4 / max(1, fusesOn)
        if auxPower < 0:
          auxPower = 0
      if power > 0 and door2:
        power -= 4 / max(1, fusesOn)
        if power < 0:
          power = 0
      elif auxPower > 0 and door2:
        auxPower -= 4 / max(1, fusesOn)
        if auxPower < 0:
          auxPower = 0
      if charge:
        charge = False
        if power > 0:
          power += 2
        elif auxPower > 0:
          auxPower += 2
      if try_activate_blackout():
        print("\n"*40)
        print("!!! BLACKOUT !!!")
        time.sleep(1.5)
      if blackout:
        # wipe ONCE
        for name in [...]:
            globals()[name] = False
        fusesOn = 0
        power = 0
      if check_death():
        print("\n"*40)
        print("!!! ALL POWER DRAINED !!!")
        print("You died.")
        input("(Press Enter to restart :D) ")
        return
      if heat:
        heat = False
        overclockHp -= 10
        print("\n"*40)
        print("!!! OVERHEAT !!!")
        print(f"Overclock HP: {overclockHp}")
        time.sleep(1.5)
      if overclockHp <= 0:
          print("\n"*40)
          print("Mitchellson: ... It's gone...\n       ... Perfect. \nI can talk to you normally now. We'll get you out of here.")
          input("\n(Press Enter to continue) ")
          return
      print("\n"*40)
      print("TIME LEFT: ##\n")
      print("-=========== OFFICE ===========-")
      print(f"Power: {int(power)}")
      print(f"Auxiliary Power: {int(auxPower)}")
      print(f"Flashlight Power: {int(flashPower)}")
      print(f"Voltage: {voltage:.2f}")
      print(f"Left Door: {door1} - Right Door: {door2}")
      print(f"\nOptions:\n1. Flashlight\n2. Open/Close Left\n3. Open/Close Right\n4. Charge Flashlight\n5. Charge Power (Aux can only be paused)\n6. Burner Phone ({'AVAILABLE' if burner else 'USED'})\n7. Breaker Box\n8. Fix Blackout (if available)\n9. OVERHEAT\n")
      choice = ""
      choice = input("Choose (number): ")
      if choice == "1":
          flashlightV2()
      elif choice == "2":
          door1 = not door1
      elif choice == "3":
          door2 = not door2
      elif choice == "4":
          flashPower = min(flashPower + random.randint(15, 30), 100)
          print("-) bweeeeee (-")
          time.sleep(1.5)
      elif choice == "5" and not door1 and not door2:
          if power > 0:
            power = min(power + random.randint(5, 15), 100)
          else:
            print("!!! POWER IS OUT, AUX CAN ONLY BE PAUSED !!!")
          print("<>< bweeeee ><>")
          charge = True
          time.sleep(1.5)
      elif choice == "5" and (door1 or door2):
          print("!!! DOORS ARE OPEN, POWER CANNOT BE CHARGED !!!")
          time.sleep(1.5)
      elif choice == "6":
          burner_phone()
          burner = False
      elif choice == "7":
          breaker_box()
          fusesOn = sum([fuse1, fuse2, fuse3, fuse4, fuse5, fuse6, fuse7, fuse8, fuse9, fuse10])
      elif choice == "8":
          timeFreeze()
      elif choice == "9":
          stockFuse()

while overclockHp > 0:
  overclock()
  power = 100
  auxPower = 100
  flashPower = 100
  door1 = False
  door2 = False
  overclockHp = 100
  charge = False
  heat = False
  blackout = False
  voltage = 0
  blackoutDistance = 15
  overclockDistance = 8
  overclockFront = 10
  overclockDoor = None
  fusesOn = 10
  fuse1 = True
  fuse2 = True
  fuse3 = True
  fuse4 = True
  fuse5 = True
  fuse6 = True
  fuse7 = True
  fuse8 = True
  fuse9 = True
  fuse10 = True
  burner = True
  timeFrozen = False