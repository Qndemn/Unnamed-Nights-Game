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
timeLeft = 50
charge = False

