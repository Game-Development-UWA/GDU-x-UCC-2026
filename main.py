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
        self.banks = 0
        self.ram = 0
        
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
    
class Message:
    def __init__(self):
        self.text = ""
        self.timer = 0
        
globalState = State()
globalLock = Lock()

message = Message()
messageLock = Lock()

loseSignal = Event()
exitSignal = Event()

def _coinChange(exitEvent: Event):
    global globalState
    while True:
        if exitEvent.is_set():
            break
        with globalLock:
            globalState.coins += round(globalState.getTrees() + 1.5 * globalState.getBanks() + 4 * globalState.getRAM())
        sleep(0.2)
        
def _quotaTimeChange(exitEvent: Event):
    global globalState
    while True:
        if exitEvent.is_set():
            break
        if globalState.curQuotaTime == 0:
            with globalLock:
                globalState.curQuotaTime = QUOTA_TIME
                
                globalState.trees -= max(2, round(globalState.getTrees() * 0.4))
                globalState.banks -= max(1, round(globalState.getBanks() * 0.4))
                globalState.ram -= max(0, round(globalState.getRAM()*0.4))
                
                if globalState.trees <= 0 and globalState.banks <= 0 and globalState.ram <= 0 and globalState.coins < 60:
                    loseSignal.set()
                
        
        sleep(0.1)
        with globalLock:
            globalState.curQuotaTime = round(globalState.curQuotaTime - 0.1, 2)

def _output(exitEvent: Event):
    global globalState
    global message
    while True:
        sleep(0.05)
        if exitEvent.is_set():
            break
        
        if message.text != "":
            with messageLock:
                message.timer = max(0, message.timer-1)
                if message.timer == 0:
                    message.text = ""

        print(f"""\n\r\033[K[ Coins (@) {globalState.coins} ]\n
           \r\033[KTrees *T* {globalState.trees}
           \r\033[KBanks [$] {globalState.banks}
           \r\033[KRAM |#$#| {globalState.ram}\n
           \r\033[KTime before next quota due - {globalState.curQuotaTime}
           \r\033[K{message.text}""")
        print("\033[9A", end="") # weird ANSI for going back two lines so illusion of static lines 
        
        if globalState.trees <= 0 and globalState.banks <= 0 and globalState.ram <= 0 and globalState.coins < 60:
            loseSignal.set()
        
def _input(exitEvent: Event):
    global globalState
    global message
    while True:
        sleep(0.05)
        if exitEvent.is_set():
            if loseSignal.is_set():
                inp = getch()
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        inp = getch()
        if exitEvent.is_set():
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        if inp == b'\x03':
            exitEvent.set()
            os.system('cls' if os.name == 'nt' else 'clear')
            break
        inp = inp.decode('utf-8')
        
        if inp == "t":
            cost = max(60, 60 + globalState.trees * 10)
            if globalState.coins >= cost:
                with globalLock:
                    globalState.coins -= cost
                    globalState.trees += 1
            else:
                message.text = f"You need {cost} coins to buy a Tree!"
                message.timer = 40
        elif inp == "b":
            cost = max(110, 110 + globalState.banks * 19)
            if globalState.coins >= cost:
                with globalLock:
                    globalState.coins -= cost
                    globalState.banks += 1
            else:
                message.text = f"You need {cost} coins to buy a Bank!"
                message.timer = 40
        elif inp == "r":
            cost = max(400, 400 + globalState.ram * 50)
            if globalState.coins >= cost:
                with globalLock:
                    globalState.coins -= cost
                    globalState.ram += 1
            else:
                message.text = f"You need {cost} coins to buy a RAM Stick!"
                message.timer = 40

def main():
    input = Thread(target=_input, args=(exitSignal,))
    output = Thread(target=_output, args=(exitSignal,))
    
    coinChange = Thread(target=_coinChange, args=(exitSignal,))
    quotaTimeChange = Thread(target=_quotaTimeChange, args=(exitSignal,))
    
    coinChange.start()
    quotaTimeChange.start()
    input.start()
    output.start()
    globalTimer = 0
    
    try:
        while True:
            sleep(0.1)
            globalTimer += 0.1
            if exitSignal.is_set():
                print("\033[2A")
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            
            if loseSignal.is_set():
                exitSignal.set()
                print("\033[9A")
                for i in range(9): print("")
                print(f"Your economy succumbed to 2026 inflation! You survived for {round(globalTimer, 2)} seconds :)")
                print("+--------------------------------------------------------------------------------------------+")
                print("Press any key to end")
                break
                
    except KeyboardInterrupt:
        exitSignal.set()
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()