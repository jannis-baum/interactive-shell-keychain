import sys, tty, termios

class InputManager:

    class ANSIParser:
        # ansi sequences: \\033\[(\d+(;\d+)*)?[A-Za-z]
        #                 ESC [ (N;...) LETTER
        
        def __init__(self, callback, callback_ansi):
            self.__callback = callback
            self.__callback_ansi = callback_ansi
            self.__reset()
        
        def __reset(self):
            self.__args = [0]
            self.__state = 0
        
        def __accept_arg(self, i):
            idx = len(self.__args) - 1
            self.__args[idx] = self.__args[idx] * 10 + i
        
        def accept(self, char):
            if char == '\033':
                self.__state = 1
                return
            
            if self.__state == 1:
                if char == '[':
                    self.__state = 2
                else:
                    self.__reset()
                return

            elif self.__state == 2:
                if char.isdigit():
                    self.__accept_arg(int(char))
                elif char == ';':
                    self.__args.append(0)
                else:
                    self.__callback_ansi(char, self.__args if self.__args != [0] else [])
                    self.__reset()
                return
            
            self.__callback(char)

    def __init__(self, callback, callback_ansi):
        self.ansiParser = InputManager.ANSIParser(callback, callback_ansi)

    def run(self):
        self.__active = True
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while self.__active:
                ch = sys.stdin.read(1)
                self.ansiParser.accept(ch)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def exit(self):
        self.__active = False

