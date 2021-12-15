# list of ansi escape codes: https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797

import sys, os
from interactive_input import InputManager
from keychain import Keychain
import config

class Interface:
    
    class Chars:
        interrupt = '0x3'
        delete = '0x7f'
        enter = '0xd'

        @staticmethod
        def compare(ch, to):
            return str(hex(ord(ch))) == to

    class ANSI: 
        up = 'A'
        down = 'B'

    def __init__(self):
        self.__query = ''
        self.__results = []
        self.__results_idx = 0
        self.__keychain = Keychain(config.SEARCH_KEYCHAINS)

        self.__chg = InputManager(self.__callback, self.__callback_ansi)
        self.__chg.run()
    
    def __callback(self, char):
        if Interface.Chars.compare(char, Interface.Chars.interrupt):
            self.__chg.exit()
            return

        elif Interface.Chars.compare(char, Interface.Chars.enter):
            if self.__results:
                self.__results[self.__results_idx].copy_password()
                self.__chg.exit()
            return

        elif Interface.Chars.compare(char, Interface.Chars.delete):
            print('\r' + ' ' * len(self.__query), end='')
            self.__query = self.__query[:-1]

        else:
            self.__query += char

        self.__results_idx = 0
        self.__refresh_output()
    
    def __callback_ansi(self, mode, args):
        if mode == Interface.ANSI.up:
            self.__results_idx = max(0, self.__results_idx - 1)
        elif mode == Interface.ANSI.down:
            self.__results_idx = min(len(self.__results) - 1, self.__results_idx + 1)
        self.__refresh_output()
        pass
    
    def __refresh_output(self):
        self.__results = self.__keychain.find_first(self.__query, 0)
        print(f"\r{' ' * os.get_terminal_size().columns}\r", end='')
        print(self.__query, end='')
        self.__print_right(
            self.__results[self.__results_idx].attributes['title']
            if self.__results else ':(')
        sys.stdout.flush()

    def __print_right(self, *args):
        print('\033[s\033[3C\033[3;33m', *args, '\033[0m\033[u', end='')
        sys.stdout.flush()
    
