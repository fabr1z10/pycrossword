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

class SpeccyTokenizer(ITokenizer):
    def __init__(self, fileName, upperCase=False):
        super().__init__(fileName, upperCase)

    def convertNumber(self, x):
        n = bytearray()
        dot = x.find('.')
        number = int(x) if dot == -1 else float(x)

        sgn = 1 if x >= 0 else -1
        # decimal part expressed in binary
        decimal_part = bin(int(abs(number)))[2:]

        #print('decimal part:',decimal_part)
        # if decimal part is non empty then
        exponent = 0
        # compute binary representation of fractional
        a = []
        if dot != -1:
            fp = number % 1
            for i in range(0,32):
                tmp = fp * 2
                a.append(int(tmp))
                fp = tmp % 1
                if fp == 0:
                    break
        mant=[]
        if decimal_part[0] == '1':
            exponent = 128 + len(decimal_part)
            mant = [int(x) for x in decimal_part]
        else:
            b = next(i for i,v in enumerate(l) if v==1)
            exponent = 128 - b
        print('exponent is ',exponent)
        mant.extend(a)
        mant = mant[:32] + [0] * (max(0, 32-len(mant)))
        # now mant is a 32 bit number
        n.append(exponent)
        print('mantissa is ', mant)
        
        for i in range(0, 4):
            n.append(int(''.join([str(x) for x in mant[8*i:8*i+8]]), 2))
        return n

            

    def save(self, lines: list, file: str):
        #print (' --- save not specified for zx-spectrum')
        print(' -- saving file: ', file)
        instructions = dict()
        #lines = self.main.toPlainText().split('\n')
        m = bytearray()
        #m += address.to_bytes(2, 'little')
        i = 0
        while i < len(lines):
            cl = lines[i]
            i += 1
            if not cl:
                continue
            lc = 0
            while cl[lc].isnumeric():
                lc += 1
            ln = int(cl[:lc])
            print(' -- parse line #',ln)
            inst = self.tokenize(cl[lc:])
            print([hex(int(x)) for x in inst])

        exit(1)

    def tokenize(self, statement: str):
        i = 0
        print(' -- parsing:',statement)
        tokens = []
        verbatim = False
        verbatim_end_char = None
        s = statement.strip()
        # preprocess string - remove spaces outside verbatim





        while i < len(s):
            # handle verbatim (e.g. DATA or quotes)
            if verbatim:
                verbatim &= (s[i] != verbatim_end_char)
                i += 1
                continue
            else:
                if s[i] in self.verbatim_start_chars:
                    verbatim = True
                    verbatim_end_char = self.verbatim_start_chars[s[i]]
                    i += 1
                    continue
            if s[i].isspace():
                i += 1
                continue
            start = i
            token = -1
            node = self.tokenRoot
            while i < len(s):
                cc = s[i].upper()
                if cc not in node.children:
                    break
                node = node.children[cc]
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
        token_inserted = False
        start_number = -1
        while i < len(s):
            if tokens and tokens[0][0] == i:
                instruction.append(tokens[0][2])
                print('FOUND TOKEN: ', tokens[0][2])
                i += tokens[0][1]
                tokens.pop(0)
                token_inserted = True
            else:
                #print('PROVA',s[i], ord(s[i]))
                if s[i].isspace() and token_inserted:
                    pass
                else:
                    if start_number == -1:
                        # check if we have a new number
                        if s[i].isdigit() or s[i] == '.':
                            start_number = i
                    else:
                        if not (s[i].isdigit() or s[i] == '.'):
                            start_number = -1
                            print('NUMBER FROM',start_number,'to',i)
                    instruction.append(self.charToCode.get(ord(s[i]), ord(s[i])))
                    token_inserted = False
                i += 1
        if start_number != -1:
            print('NUMBER FROM',start_number,'to',i)
            nr = self.convertNumber(s[start_number:i])
            print('number:', [hex(int(x)) for x in nr])

        return instruction


class C64Tokenizer(ITokenizer):
    def __init__(self, fileName, upperCase=False):
        super().__init__(fileName, upperCase)

    def save(self, lines: list, file: str):
        print(' -- saving file: ', file)
        # address of next instruction
        address = 0x0801
        instructions = dict()
        #lines = self.main.toPlainText().split('\n')
        m = bytearray()
        m += address.to_bytes(2, 'little')
        i = 0
        while i < len(lines):
            cl = lines[i]
            i += 1
            if not cl:
                continue
            lc = 0
            while cl[lc].isnumeric():
                lc += 1
            print('line number ends @ ', lc, ': ', cl[:lc])
            inst = self.tokenize(cl[lc:])
            print(' # bytes:', len(inst))
            # 4 bytes are occupied to hold address of next BASIC instruction and the line number
            # 1 byte is the 0 at the end of inst
            address += len(inst) + 4 + 1
            ln = int(cl[:lc])
            line_number = ln.to_bytes(2, 'little')
            next_inst = address.to_bytes(2, 'little')
            instruction = bytearray()
            instruction += next_inst
            instruction += line_number
            instruction += inst
            instruction.append(0)
            print(' '.join(f'{x:02x}' for x in instruction))
            instructions[ln] = instruction
            # f.write(instruction)
        sorted_instructions = sorted(instructions)  # [x[1] for x in sorted(instructions.items())]
        for s in sorted_instructions:
            print(int(s), ': ', ' '.join(f'{x:02x}' for x in instructions[s]))
        # print(sorted_instructions)
        # do the proper writing
        with open(file, 'wb') as f:
            address = 0x0801
            m = address.to_bytes(2, 'little')
            f.write(m)
            for s in sorted_instructions:
                f.write(instructions[s])
            m = bytearray()
            m.append(0)
            m.append(0)
            f.write(m)

    def load(self, file):
        li = {}
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


class Tokenizer(ITokenizer):
    def __init__(self, fileName, upperCase=False):
        super().__init__(fileName, upperCase)
        #print(' -- tokenizer: ', fileName)
        #with open(fileName, 'r') as file:
        #    self.tokens = yaml.safe_load(file)
        #self.tokenRoot = TokenNode()
        #self.invOrd = dict()
        #for token, value in self.tokens['tokens'].items():
        #    self.invTokens[value] = token
        # for token, value in self.tokens['ord'].items():
        #     self.invOrd[value] = token
        #for sc in self.tokens['special_chars']:
        #    self.charToCode[sc['char']] = sc['code']
        #    self.codeToChar[sc['code']] = sc['char']
        #    self.keys[(sc['mod'], sc['key'])] = sc['char']
        #    print(sc)
        # create tree
        # for token, value in self.tokens['tokens'].items():
        #     node = self.tokenRoot
        #     i = 0
        #     while i < len(token):
        #         if token[i] not in node.children:
        #             node.children[token[i]] = TokenNode()
        #         node = node.children[token[i]]
        #         if i == len(token) - 1:
        #             node.token = value
        #         i += 1



    # def tokenize(self, s: str):
    #     i = 0
    #     tokens = []
    #     in_quotes = False
    #     verbatim = False
    #     while i < len(s):
    #         if verbatim:
    #             verbatim &= s[i] != ":"
    #             i += 1
    #             continue
    #         if s[i] == "\"":
    #             in_quotes = not in_quotes
    #             i += 1
    #             continue
    #         start = i
    #         #print('trying token starting @', start)
    #         token = -1
    #         node = self.tokenRoot
    #         while not in_quotes and i < len(s):
    #             if s[i] not in node.children:
    #                 break
    #             node = node.children[s[i]]
    #             token = node.token
    #             i += 1
    #         if token != -1:
    #             tokens.append((start, i - start, token))
    #             #print('found token @', start, (i - start), ':', token)
    #             if token == 131:  # data
    #                 verbatim = True
    #         else:
    #             i = start + 1
    #         #    i += 1
    #     i = 0
    #     instruction = bytearray()
    #     while i < len(s):
    #         if tokens and tokens[0][0] == i:
    #             instruction.append(tokens[0][2])
    #             i += tokens[0][1]
    #             tokens.pop(0)
    #         else:
    #             print('PROVA',s[i], ord(s[i]))
    #             instruction.append(self.charToCode.get(ord(s[i]), ord(s[i])))
    #             i += 1
    #     return instruction

