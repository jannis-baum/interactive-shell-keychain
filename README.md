# Interactive Shell Keychain Access

Run `$ ./main.py` to live search through Mac Keychains specified in `config.py`. Search results can be scrolled through using the arrow keys. Hitting `Return` will copy the selected item's password to the clipboard and exit the script. To exit without copying a password, hit `Control-C`.

## Accessing iCloud Keychain

MacOS currently doesn't allow the underlying utility program `$ security` to access iCloud Keychains. Since MacOS Monterey, iCloud passwords can however be manually exported as an unencrypted `.csv` file (e.g. through Safari → Export → Passwords). This file `Passwords.csv` can then be imported into a local Keychain by using
```shell
$ import_passwords.py Passwords.csv
```
Note that you will be asked to provide a password for the Keychain that'll be created. This Keychain (by default `icloud-local.keychain`) is then accessible through this script.

