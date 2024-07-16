from PySide6.QtCore import Qt
import yaml

class TokenNode:
    def __init__(self):
        self.token = -1
        self.children = dict()

    def add(self, character, token):
        self.children[character] = token

# abstract tokenizer class
class ITokenizer:
    def tokenize(self, statement: str):
        i = 0
        tokens = []
        verbatim = False
        verbatim_end_char = None
        s = statement.strip()
        while i < len(s):
            # handle verbatim (e.g. DATA or quotes)
            if verbatim:
                verbatim &= (s[i] != verbatim_end_char)
                i += 1
                continue
            else:
                if s[i] in self.verbatim_start_chars:
                    print('ENTERING VERBA')
                    verbatim = True
                    verbatim_end_char = self.verbatim_start_chars[s[i]]
                    i += 1
                    continue
            start = i
            token = -1
            node = self.tokenRoot
            while i < len(s):
                if s[i] not in node.children:
                    break
                node = node.children[s[i]]
                token = node.token
                i += 1
            if token != -1:
                tokens.append((start, i - start, token))
                if token in self.verbatim_start_tokens:
                    verbatim = True
                    self.verbatim_end_char = self.verbatim_start_tokens[token]
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
    def __init__(self, fileName, upperCase=False):
        print(' -- tokenizer: ', fileName)
        # first of all we need a list of all tokens (e.g. PRINT, POKE etc)
        with open(fileName, 'r') as file:
            self.tokens = yaml.safe_load(file)
        # create tree
        self.tokenRoot = TokenNode()
        self.invTokens = dict()
        self.charToCode = dict()
        self.codeToChar = dict()
        self.keys = dict()
        self.verbatim_start_chars = {}
        self.verbatim_start_tokens = {}
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
        for token, value in self.tokens['tokens'].items():
            self.invTokens[value] = token
        # Handle special chars
        for sc in self.tokens['special_chars']:
            self.charToCode[sc['char']] = sc['code']
            self.codeToChar[sc['code']] = sc['char']
            self.keys[(sc['mod'], sc['key'])] = sc['char']
            #print(sc)
        if upperCase:
            for i in range(Qt.Key_A, Qt.Key_Z+1):
                self.keys[(Qt.NoModifier.value, i)] = i
        if 'verbatim_start_chars' in self.tokens:
            for key, value in self.tokens['verbatim_start_chars'].items():
                self.verbatim_start_chars[key] = value
        if 'verbatim_start_tokens' in self.tokens:
            for key, value in self.tokens['verbatim_start_tokens'].items():
                self.verbatim_start_tokens[key] = value






# class Tokenizer(ITokenizer):
#     def __init__(self, fileName, upperCase=False):
#         super().__init__(fileName, upperCase)
#         #print(' -- tokenizer: ', fileName)
#         #with open(fileName, 'r') as file:
#         #    self.tokens = yaml.safe_load(file)
#         #self.tokenRoot = TokenNode()
#         #self.invOrd = dict()
#         #for token, value in self.tokens['tokens'].items():
#         #    self.invTokens[value] = token
#         # for token, value in self.tokens['ord'].items():
#         #     self.invOrd[value] = token
#         #for sc in self.tokens['special_chars']:
#         #    self.charToCode[sc['char']] = sc['code']
#         #    self.codeToChar[sc['code']] = sc['char']
#         #    self.keys[(sc['mod'], sc['key'])] = sc['char']
#         #    print(sc)
#         # create tree
#         # for token, value in self.tokens['tokens'].items():
#         #     node = self.tokenRoot
#         #     i = 0
#         #     while i < len(token):
#         #         if token[i] not in node.children:
#         #             node.children[token[i]] = TokenNode()
#         #         node = node.children[token[i]]
#         #         if i == len(token) - 1:
#         #             node.token = value
#         #         i += 1
#
#
#
#     # def tokenize(self, s: str):
#     #     i = 0
#     #     tokens = []
#     #     in_quotes = False
#     #     verbatim = False
#     #     while i < len(s):
#     #         if verbatim:
#     #             verbatim &= s[i] != ":"
#     #             i += 1
#     #             continue
#     #         if s[i] == "\"":
#     #             in_quotes = not in_quotes
#     #             i += 1
#     #             continue
#     #         start = i
#     #         #print('trying token starting @', start)
#     #         token = -1
#     #         node = self.tokenRoot
#     #         while not in_quotes and i < len(s):
#     #             if s[i] not in node.children:
#     #                 break
#     #             node = node.children[s[i]]
#     #             token = node.token
#     #             i += 1
#     #         if token != -1:
#     #             tokens.append((start, i - start, token))
#     #             #print('found token @', start, (i - start), ':', token)
#     #             if token == 131:  # data
#     #                 verbatim = True
#     #         else:
#     #             i = start + 1
#     #         #    i += 1
#     #     i = 0
#     #     instruction = bytearray()
#     #     while i < len(s):
#     #         if tokens and tokens[0][0] == i:
#     #             instruction.append(tokens[0][2])
#     #             i += tokens[0][1]
#     #             tokens.pop(0)
#     #         else:
#     #             print('PROVA',s[i], ord(s[i]))
#     #             instruction.append(self.charToCode.get(ord(s[i]), ord(s[i])))
#     #             i += 1
#     #     return instruction
#
