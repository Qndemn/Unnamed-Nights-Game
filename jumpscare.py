import os
import time
import sys

def clear_screen():
    # Clears the terminal screen for smooth animation windows/unix
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # 1. The initial smiling mouth
    smile = """
    
    
          \\___________/          
    
    
    """

    # 2. The mouth opens wide
    mouth_open = """
           /XXXXXXXXX\\           
          /           \\          

         |             |         
          \\           /          
           \\_________/           
    """

    # 3. The bite down (sharp teeth clenching)
    bite = """
           /vvvvvvvvv\\           
          < XXXXXXXXX >          
           \\^^^^^^^^^/           
    """

    try:
        # Step 1: Start with just the smiling mouth
        clear_screen()
        print(smile)
        sys.stdout.flush()
        time.sleep(2.0)  # Holds the smile for anticipation

        # Step 2: The mouth opens up
        clear_screen()
        print(mouth_open)
        sys.stdout.flush()
        time.sleep(1.5)  # Stays open for a brief, tense pause

        # Step 3: BITES DOWN snaps shut quickly
        clear_screen()
        print(bite)
        sys.stdout.flush()
        time.sleep(0.1)  # Fast bite dynamic
        
    except KeyboardInterrupt:
        print("\nAnimation skipped.")