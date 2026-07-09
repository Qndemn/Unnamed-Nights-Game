import sys, select, tty, termios, threading, time, random, os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def stockFuse():
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
        clear()
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
        print("=== STOCKFUSE INITIATED ===\n")

        threading.Thread(target=drain_fuses, daemon=True).start()
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
                    return

                # TIME OUT = failure
                if time_up:
                    print("\nFAILURE: Time ran out.")
                    break

                # Burnout: ANY fuse hitting 0% = death
                for f in fuses:
                    if f <= 0.0:
                        running = False
                        print("\nFAILURE: A fuse burned out.")
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

stockFuse()