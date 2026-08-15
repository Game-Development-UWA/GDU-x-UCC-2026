from threading import Thread

def _staticLine(string: str) -> str:
    return f"\r{string}"

def _input():
    while True:
        inp = input(_staticLine("Action: "))
        print("\033[1A\033[K", end="") #weird ANSI for going back to last line so illusion of static line
        if inp == 'q':
            break


def main():
    input = Thread(target=_input)
    input.start()



if __name__ == "__main__":
    main()
