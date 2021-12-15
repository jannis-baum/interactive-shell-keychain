import yaml, subprocess, re

class KeychainReader:
    class KeychainItem:
        search_atts = {
            'title': r'^\s*0x00000007 <blob>="([^"]*)"$',
            'account': r'\s*"acct"<blob>="([^"]*)"$',
            'server': r'^\s*"srvr"<blob>="([^"]*)"$'
        }

        def __init__(self, attributes):
            self.attributes = {
                key: (lambda m: m.group(1) if m else None)(re.search(reg, attributes, re.MULTILINE))
            for key, reg in KeychainReader.KeychainItem.search_atts.items() }
        
    splitter = 'keychain: '

    def __init__(self, keychains):
        dumped = ''.join([
            subprocess.check_output(f'/usr/bin/security dump-keychain {keychain}', shell=True).decode('utf-8')
        for keychain in keychains])
        self.kc_items = self.__parse(dumped)
    
    def __parse(self, dumped):
        return [
            KeychainReader.KeychainItem(KeychainReader.splitter + block)
        for block in dumped.split(KeychainReader.splitter) if block]

    def find_first(self, query, count = 1):
        res = list()
        for kc_item in self.kc_items:
            if [item for item in kc_item.attributes.values() if item and query in item]:
                res.append(kc_item)
                if len(res) == count: return res
        return res

