# list of ansi escape codes: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797

import sys
from input_manager import InputManager
from keychain import Keychain

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
        self.__results = []
        self.__keychain = Keychain([ 'icloud-local.keychain', 'login.keychain'])
        self.__chg = InputManager(self.__callback, self.__callback_ansi)
        self.__chg.run()
    
    def __callback(self, char):
        if Interface.Chars.compare(char, Interface.Chars.interrupt):
            self.__chg.exit()
            return

        elif Interface.Chars.compare(char, Interface.Chars.enter):
            if self.__results:
                self.__results[0].copy_password()
                self.__chg.exit()
            return

        elif Interface.Chars.compare(char, Interface.Chars.delete):
            print('\r' + ' ' * len(self.__query), end='')
            self.__query = self.__query[:-1]

        else:
            self.__query += char

        print('\r' + self.__query, end='')
        self.__results = self.__keychain.find_first(self.__query, 0)
        self.__print_right(
            (lambda r: r[0].attributes['title'] if r else ':(')
            (self.__keychain.find_first(self.__query))
        )
        sys.stdout.flush()
    
    def __callback_ansi(self, mode, args):
        pass
    
    def __print_right(self, *args):
        print('\033[s\033[3C\033[3;33m', *args, '\033[0m\033[u', end='')
        sys.stdout.flush()

