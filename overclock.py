import random
import time
import sys
from inputimeout import inputimeout, TimeoutOccurred
import math
import threading
import select
import tty
import termios

inputs = ["1", "2", "3"]
power = 100
auxPower = 100
flashPower = 100
door1 = False
door2 = False
timeLeft = 500
charge = False
heat = 0
voltage = 0
blackoutDistance = 15
overclockDistance = 0
overclockFront = 0
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

def breaker_box():
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
        global fuse1
        fuse1 = not fuse1
    elif fuseChosen == "2":
        global fuse2
        fuse2 = not fuse2
    elif fuseChosen == "3":
        global fuse3
        fuse3 = not fuse3
    elif fuseChosen == "4":
        global fuse4
        fuse4 = not fuse4
    elif fuseChosen == "5":
        global fuse5
        fuse5 = not fuse5
    elif fuseChosen == "6":
        global fuse6
        fuse6 = not fuse6
    elif fuseChosen == "7":
        global fuse7
        fuse7 = not fuse7
    elif fuseChosen == "8":
        global fuse8
        fuse8 = not fuse8
    elif fuseChosen == "9":
        global fuse9
        fuse9 = not fuse9
    elif fuseChosen == "10":
        global fuse10
        fuse10 = not fuse10

def flashlightV2():
    global flashPower, overclockFront
    if flashPower > 0:
        flashPower -= 25
        print(f"Overclock: {overclockFront}")
        overclockFront = "reset"
        print("(<<< FLASH >>>)")
    else:
        print("!!! OUT OF FLASHLIGHT POWER !!!")

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

def shortFuse():
    global timeFrozen, power, voltage
    duration_seconds = 20
    FUSE_COUNT = 5
    DRAIN_RATE = 0.015 / (duration_seconds / 30)
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
        nonlocal running, time_up, fuses, time_left

        start = time.time()
        print("!!! TIME FROZEN !!!")
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
                print("\nSUCCESS: Time Unfrozen.")
                timeFrozen = False
            else:
                print("\nFAILURE: A fuse burned out.")
                power -= 15
                voltage += 0.1

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            running = False

        print("\nShortFuse Challenge Ended.")

    shortfuse_minigame(duration_seconds)

def timeFreeze():
    if timeFrozen:
        print("Ready?")
        input("(Enter to start minigame) ")
        shortFuse()
    else:
        print("!! TIME ISN'T FROZEN !!")

def stockFuse():
    global power, voltage, timeFrozen
    duration_seconds = 26
    FUSE_COUNT = 5

    # Fuses start at 25%
    fuses = [0.25] * FUSE_COUNT

    # Tuned drain + boost values
    DRAIN_RATE = 0.0028
    BOOST_AMOUNT = 0.3
    TICK_SPEED = 0.035

    running = True
    time_left = 0
    time_up = False

    def drain_fuses():
        """Drain only fuses above 25%, smooth and reversible."""
        nonlocal running, fuses
        while running:
            for i in range(FUSE_COUNT):
                if fuses[i] > 0.25 and fuses[i] < 1.0:
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
        nonlocal running, time_up, fuses, time_left

        start = time.time()
        print("!!! TIME FROZEN !!!")
        print(f"StockFuse Challenge Started ({duration_seconds} seconds)\n")

        # Start fuse drain
        threading.Thread(target=drain_fuses, daemon=True).start()

        # Start real-time countdown
        threading.Thread(target=countdown_timer, args=(duration_seconds,), daemon=True).start()

        # Enable raw input mode
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)

        current_prompt = choose_fuse_prompt()

        try:
            while running:
                time_left = round(duration_seconds - (time.time() - start), 1)
                print_fuses(current_prompt)

                # WIN CONDITION: all fuses at 100%
                if all(f >= 1.0 for f in fuses):
                    running = False
                    print("\nSUCCESS: All fuses stabilized at 100%.")
                    timeFrozen = False
                    return

                # TIME OUT = failure
                if time_up:
                    print("\nFAILURE: Time ran out.")
                    power -= 15
                    voltage += 0.1
                    break

                # Burnout: ANY fuse hitting 0% = death
                for f in fuses:
                    if f <= 0.0:
                        running = False
                        print("\nFAILURE: A fuse burned out.")
                        power -= 15
                        voltage += 0.1
                        return

                # True ShortFuse input
                key = get_key()
                if key and key.isdigit():
                    idx = int(key) - 1

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

    stockfuse_minigame(duration_seconds)