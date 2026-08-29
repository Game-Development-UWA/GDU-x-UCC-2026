from threading import Thread, Lock, Event
import random
import os
from time import sleep

class State:
    def __init__(self):
        self.coins = 10
        self.rate = 1
        
globalState = State()
globalLock = Lock()

exitSignal = Event()

def _coinChange(exitEvent: Event):
    global globalState
    while True:
        if exitEvent.is_set():
            break
        with globalLock:
            globalState.coins = int(globalState.coins * globalState.rate)
        sleep(0.2)
            
def _rateChange(exitEvent: Event):
    global globalState
    while True:
        if exitEvent.is_set():
            break
        with globalLock:
            globalState.rate = round(0.9 + random.random()*0.6, 7)
        sleep(0.2)

def _input(exitEvent: Event):
    global globalState
    while True:
        sleep(0.05)
        """inp = input(_staticLine("Action: "))
        print("\033[1A\033[K", end="") #weird ANSI for going back to last line so illusion of static line
        if inp == 'q':
            break"""
        if exitEvent.is_set():
            break
        print(f"Coins - {globalState.coins} |")
        print(f"Rate - {globalState.rate}")
        print("\033[2A", end="")

def main():
    input = Thread(target=_input, args=(exitSignal,))
    coinChange = Thread(target=_coinChange, args=(exitSignal,))
    rateChange = Thread(target=_rateChange, args=(exitSignal,))
    rateChange.start()
    coinChange.start()
    input.start()
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        exitSignal.set()
        print("\033[2A")
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()