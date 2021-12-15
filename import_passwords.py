#!/usr/bin/env python3

import csv, subprocess, argparse

KEYCHAIN_NAME = 'icloud-local.keychain'

def resetKeychain():
    subprocess.call(['security', 'delete-keychain', KEYCHAIN_NAME], stderr=subprocess.DEVNULL)
    subprocess.call(['security', 'create-keychain', KEYCHAIN_NAME])
    # add stop if password incorrect

def importPasswords(source):
    resetKeychain()
    with open(source, 'r') as fp:
        reader = csv.reader(fp)
        idx = { f: n for n, f in enumerate(next(reader)) }
        for row in reader:
            params = ['-l', row[idx['Title']], '-a', row[idx['Username']], '-s', row[idx['Url']], '-w', row[idx['Password']]]
            subprocess.call(['security', 'add-internet-password'] + params + [KEYCHAIN_NAME])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('passwords', type=str)
    args = parser.parse_args()
    importPasswords(args.passwords)

