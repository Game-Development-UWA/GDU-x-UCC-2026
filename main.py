from threading import Thread, Lock, Event
import random
import os
from msvcrt import getch

from time import sleep

QUOTA_TIME = 15

class State:
    def __init__(self):
        self.coins = 10
        
        self.trees = 5
        self.banks = -1
        self.ram = -1
        
        self.curQuotaTime = QUOTA_TIME
    
    def getTrees(self):
        if self.trees < 0:
            return 0
        return self.trees
    
    def getBanks(self):
        if self.banks < 0:
            return 0
        return self.banks
    
    def getRAM(self):
        if self.ram < 0:
            return 0
        return self.ram
        
globalState = State()
globalLock = Lock()

exitSignal = Event()

def _coinChange(exitEvent: Event):
    global globalState
    while True:
        if exitEvent.is_set():
            break
        with globalLock:
            globalState.coins += globalState.getTrees() + 1.5 * globalState.getBanks() + 4 * globalState.getRAM()
        sleep(0.2)
            
def _treeChange(exitEvent: Event):
    global globalState
    while True:
        if exitEvent.is_set():
            break
        with globalLock:
            globalState.trees
        sleep(0.2)
        
def _bankChange(exitEvent: Event):
    global globalState
    while True:
        if exitEvent.is_set():
            break
        with globalLock:
            globalState.banks
        sleep(0.2)

def _ramChange(exitEvent: Event):
    global globalState
    while True:
        if exitEvent.is_set():
            break
        with globalLock:
            globalState.ram
        sleep(0.2)
        
def _quotaTimeChange(exitEvent: Event):
    global globalState
    while True:
        if exitEvent.is_set():
            break
        if globalState.curQuotaTime == 0:
            globalState.curQuotaTime = QUOTA_TIME
            
            globalState.trees -= 4
            if globalState.banks != -1:
                globalState.banks -= 2
            if globalState.ram != -1:
                globalState.ram -= 1
        
        sleep(0.1)
        with globalLock:
            globalState.curQuotaTime = round(globalState.curQuotaTime - 0.1, 2)

def _output(exitEvent: Event):
    global globalState
    while True:
        sleep(0.05)
        if exitEvent.is_set():
            break
        print(f"\rCoins - {globalState.coins}")
        print(f"\rTrees - {globalState.trees} | Banks - {globalState.banks} | RAM - {globalState.ram}")
        print(f"\rTime before next quota due - {globalState.curQuotaTime}")
        print("\033[3A", end="") # weird ANSI for going back two lines so illusion of static lines
        
def _input(exitEvent: Event):
    global globalState
    while True:
        sleep(0.05)
        if exitEvent.is_set():
            break
        inp = getch()
        if inp == b'\x03':
            exitEvent.set()
            break
        

        
        
def main():
    input = Thread(target=_input, args=(exitSignal,))
    output = Thread(target=_output, args=(exitSignal,))
    
    coinChange = Thread(target=_coinChange, args=(exitSignal,))
    treeChange = Thread(target=_treeChange, args=(exitSignal,))
    bankChange = Thread(target=_bankChange, args=(exitSignal,))
    ramChange = Thread(target=_ramChange, args=(exitSignal,))
    quotaTimeChange = Thread(target=_quotaTimeChange, args=(exitSignal,))
    
    treeChange.start()
    bankChange.start()
    ramChange.start()
    coinChange.start()
    quotaTimeChange.start()
    input.start()
    output.start()
    
    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        exitSignal.set()
        print("\033[2A")
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()