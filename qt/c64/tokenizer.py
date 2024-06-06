from PySide6.QtCore import Qt
import yaml

class TokenNode:
    def __init__(self):
        self.token = -1
        self.children = dict()

    def add(self, character, token):
        self.children[character] = token

class Tokenizer:
    def __init__(self, fileName, upperCase=False):
        print(' -- tokenizer: ', fileName)
        with open(fileName, 'r') as file:
            self.tokens = yaml.safe_load(file)
        self.tokenRoot = TokenNode()
        self.invTokens = dict()
        self.charToCode = dict()
        self.codeToChar = dict()
        self.keys = dict()
        #self.invOrd = dict()
        for token, value in self.tokens['tokens'].items():
            self.invTokens[value] = token
        # for token, value in self.tokens['ord'].items():
        #     self.invOrd[value] = token
        for sc in self.tokens['special_chars']:
            self.charToCode[sc['char']] = sc['code']
            self.codeToChar[sc['code']] = sc['char']
            self.keys[(sc['mod'], sc['key'])] = sc['char']
            print(sc)
        if upperCase:
            for i in range(Qt.Key_A, Qt.Key_Z+1):
                self.keys[(Qt.NoModifier.value, i)] = i
        # create tree
        for token, value in self.tokens['tokens'].items():
            node = self.tokenRoot
            i = 0
            while i < len(token):
                if token[i] not in node.children:
                    node.children[token[i]] = TokenNode()
                node = node.children[token[i]]
                if i == len(token) - 1:
                    node.token = value
                i += 1

    def tokenize(self, s: str):
        i = 0
        tokens = []
        in_quotes = False
        verbatim = False
        while i < len(s):
            if verbatim:
                verbatim &= s[i] != ":"
                i += 1
                continue
            if s[i] == "\"":
                in_quotes = not in_quotes
                i += 1
                continue
            start = i
            #print('trying token starting @', start)
            token = -1
            node = self.tokenRoot
            while not in_quotes and i < len(s):
                if s[i] not in node.children:
                    break
                node = node.children[s[i]]
                token = node.token
                i += 1
            if token != -1:
                tokens.append((start, i - start, token))
                #print('found token @', start, (i - start), ':', token)
                if token == 131:  # data
                    verbatim = True
            else:
                i = start + 1
            #    i += 1
        i = 0
        instruction = bytearray()
        while i < len(s):
            if tokens and tokens[0][0] == i:
                instruction.append(tokens[0][2])
                i += tokens[0][1]
                tokens.pop(0)
            else:
                print('PROVA',s[i], ord(s[i]))
                instruction.append(self.charToCode.get(ord(s[i]), ord(s[i])))
                i += 1
        return instruction

    def readBasicFile(self, file):
        #print(settings.invtoken)
        li = {}
        #print(self.invOrd)
        with open(file, 'rb') as f:
            address = f.read(2)
            a0 = int.from_bytes(address, 'little')
            if int(address[0]) == 0x01 and int(address[1]) == 0x08:
                print(' -- found BASIC Program.')
            while True:
                address = f.read(2)
                a1 = int.from_bytes(address, 'little')
                if a1 == 0:
                    break
                length = a1 - a0
                # read line number
                ln = int.from_bytes(f.read(2), 'little')
                #print('---')
                #print('line number:', ln)
                #print('length of current inst: ', length)
                data = f.read(length - 4)[:-1]  # drop last byte
                m = [str(ln), ' ']
                in_quotes = False
                for b in data:
                    if int(b) == ord('"'):
                        in_quotes = not in_quotes
                    #used_map = self.invOrd if in_quotes else self.invTokens
                    if in_quotes:
                        m.append(chr(self.codeToChar.get(b, b)))
                    else:
                        if b in self.invTokens:
                            m.append(self.invTokens[b])
                        else:
                            m.append(chr(self.codeToChar.get(b, b)))

                    #m.append(chr(used_map.get(int(b), b)))
                print(m)
                inst = ''.join(m)
                print(inst)
                li[ln] = inst
                a0 = a1
        return li
