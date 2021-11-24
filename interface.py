import sys
from input_manager import InputManager

class Interface:
    
    class Chars:
        interrupt = '0x3'
        delete = '0x7f'
        enter = '0xd'

        @staticmethod
        def compare(ch, to):
            return str(hex(ord(ch))) == to

    def __init__(self):
        self.__query = ''
        self.__chg = InputManager(self.__callback, self.__callback_ansi)
        self.__chg.run()
    
    def __callback(self, char):
        if Interface.Chars.compare(char, Interface.Chars.interrupt):
            self.__chg.exit()
            return
        elif Interface.Chars.compare(char, Interface.Chars.enter):
            return
        elif Interface.Chars.compare(char, Interface.Chars.delete):
            print('\r' + ' ' * len(self.__query), end='')
            self.__query = self.__query[:-1]
        else:
            self.__query += char
        print('\r' + self.__query, end='')
        self.__exec_with_cursor_pos(self.__print_right)
        sys.stdout.flush()
    
    def __callback_ansi(self, mode, args):
        if mode == 'R':
            self.__ewcp(args)

    def __exec_with_cursor_pos(self, exec):
        self.__ewcp = exec
        print('\033[6n', end='')
    
    def __print_right(self, *args):
        print('\033[s\033[3C\033[3;33m', *args, '\033[0m\033[u', end='')
        sys.stdout.flush()
