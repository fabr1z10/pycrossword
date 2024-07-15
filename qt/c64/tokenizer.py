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

class SpeccyTokenizer(ITokenizer):
    def __init__(self, fileName, upperCase=False):
        super().__init__(fileName, upperCase)

    # provides the  5-byte numeric format of a number given in str format
    def convertNumber(self, x: str):
        n = bytearray()
        dot = x.find('.')
        print('number is a: ', 'int' if dot == -1 else 'float')
        number = int(x) if dot == -1 else float(x)
        dp = int(abs(number))
        sgn = 1 if number >= 0 else -1
        # decimal part expressed in binary
        decimal_part = bin(dp)[2:]

        print('decimal part:',decimal_part)
        # if decimal part is non empty then
        exponent = 0
        # compute binary representation of fractional


        a = [] if dp == 0 else [int(x) for x in list(decimal_part)]
        # if we have a fractionary part. stop when we have 32 digits
        index_of_first_one = 0 if dp > 0 else -1
        point_index = len(a)
        #print('a=',a)
        if dot != -1:
            fp = number % 1
            k = 0
            while len(a) < 33:
                tmp = fp * 2
                # don't add leading zeros if we have no decimal part
                cn = int(tmp)
                #print(tmp,cn,index_of_first_one)
                if index_of_first_one == -1:
                    if cn == 1:
                        index_of_first_one = k
                        a.append(cn)
                else:
                    a.append(cn)
                fp = tmp % 1
                k += 1
                if fp == 0:
                    break
            exponent = point_index - index_of_first_one
            print(len(a))
            #a += [0] * (max(0, 33-len(a)))
            # apply carry
            klol= int(''.join([str(x) for x in a[:32]]), 2)
            mantissa = bin(klol+a[32])[2:]
            print(mantissa)
            # now mant is a 32 bit number
            # first nbit of mantissa is always 1 - override with sign
            mantissa = ('0' if sgn > 0 else '1') + mantissa[1:]
            print('mantissa is ', mantissa)
            n.append (128 + exponent)
            for i in range(0, 4):
                n.append(int(mantissa[8*i:8*i+8], 2))
            return n
        else:
            #  1 byte: always 0
            n.append(0)
            #  1 byte: 0 if the number is positive or -1 (0xFF) if the number is negative
            n.append(0 if sgn == 1 else 0xFF)
            #  2 bytes: little-endian unsigned integer from 0 to 65535.
            #  Subtract 65536 from this if number is flagged as negative
            nn = number if sgn == 1 else number - 65536
            n += nn.to_bytes(2, 'little')
            #  1 byte: always 0
            n.append(0)

            return n

            

    def save(self, lines: list, file: str):
        #print (' --- save not specified for zx-spectrum')
        print(' -- saving file: ', file)
        instructions = dict()
        #lines = self.main.toPlainText().split('\n')
        m = bytearray()
        #m += address.to_bytes(2, 'little')
        i = 0
        total_length = 0
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
            linst = len(inst)
            instruction = bytearray()
            instruction += ln.to_bytes(2, 'big')
            instruction += linst.to_bytes(2, 'little')
            instruction += inst
            instructions[ln] = instruction
            total_length += len(instruction)
        sorted_instructions = sorted(instructions)  # [x[1] for x in sorted(instructions.items())]
        print('total length:',hex(total_length))
        #with open(file, 'wb') as f:
        #    for s in sorted_instructions:
        #        f.write(instructions[s])



    def tokenize(self, statement: str):
        i = 0
        print(' -- parsing:',statement)
        tokens = []
        verbatim = False
        verbatim_end_char = None
        s = statement.strip()

        instruction = bytearray()

        current_number = []
        while i < len(s):
            # handle verbatim (e.g. DATA or quotes)
            if verbatim:
                verbatim &= (s[i] != verbatim_end_char)
                instruction.append(s[i])
                i += 1
                continue
            else:
                if s[i] in self.verbatim_start_chars:
                    verbatim = True
                    verbatim_end_char = self.verbatim_start_chars[s[i]]
                    instruction.append(s[i])
                    i += 1
                    continue
            start = i
            token = -1
            node = self.tokenRoot
            while i < len(s):
                if s[i].isspace():
                    i += 1
                    continue
                cc = s[i].upper()
                if cc not in node.children:
                    break
                node = node.children[cc]
                token = node.token
                i += 1
            if token != -1:
                instruction.append(token)
                #tokens.append((start, i - start, token))
                if token in self.verbatim_start_tokens:
                    verbatim = True
                    self.verbatim_end_char = self.verbatim_start_tokens[token]
            else:
                if not current_number and s[i].isdigit():
                    current_number = [s[i]]
                elif current_number:
                    if s[i].isdigit() or s[i] == '.':
                        current_number.append(s[i])
                    else:
                        instruction.append(0x0E)
                        instruction += self.convertNumber(''.join(current_number))
                        current_number = None
                instruction.append(self.charToCode.get(ord(s[i]), ord(s[i])))
                #instruction.append(s[i])
                i = start + 1
            #    i += 1
        if current_number != -1:
            instruction.append(0x0E)
            instruction += self.convertNumber(''.join(current_number))
        instruction.append(0x0D)
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

