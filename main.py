from threading import Thread, Lock
import random
from time import sleep

class State:
    def __init__(self):
        self.coins = 10
        self.rate = 1
        
globalState = State()
globalLock = Lock()

def _staticLine(string: str) -> str:
    return f"\r{string}"

def _coinChange():
    global globalState
    while True:
        with globalLock:
            globalState.coins = int(globalState.coins * globalState.rate)
        sleep(0.2)
            
def _rateChange():
    global globalState
    while True:
        with globalLock:
            globalState.rate = round(0.9 + random.random()*0.6, 7)
        sleep(0.2)

def _input():
    global globalState
    while True:
        """inp = input(_staticLine("Action: "))
        print("\033[1A\033[K", end="") #weird ANSI for going back to last line so illusion of static line
        if inp == 'q':
            break"""
        print(f"\r Coins - {globalState.coins} | Rate - {globalState.rate}", end="")
        #if globalState.rate >= 1.5:
           # print('end')
            #break

def main():
    input, coinChange, rateChange = Thread(target=_input), Thread(target=_coinChange), Thread(target=_rateChange)
    rateChange.start()
    coinChange.start()
    input.start()



if __name__ == "__main__":
    main()
