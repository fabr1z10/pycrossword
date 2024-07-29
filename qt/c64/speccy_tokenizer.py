from tokenizer import ITokenizer
from pathlib import Path

class SpeccyTokenizer(ITokenizer):
    def __init__(self, fileName, upperCase=False):
        super().__init__(fileName, upperCase)

    # provides the  5-byte numeric format of a number given in str format
    def convertNumber(self, x: str):
        print('converting',x)
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
            print(len(a),a)
            a += [0] * (max(0, 33-len(a)))
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

    def checksum(self, l: list):
        chksum=0
        for d in l:
            chksum ^= d
        return chksum

    def load(self, file):
        li = {}
        with open(file, 'rb') as f:
            address = f.read(24)
            while True:
                lno = f.read(2)
                if lno == '':
                    break
                ln = int.from_bytes(lno, 'big')
                length = int.from_bytes(f.read(2), 'little')
                if length == 0:
                    break
                print('reading line number:',ln,'len:',length)
                # address = f.read(2)
                # a1 = int.from_bytes(address, 'little')
                # if a1 == 0:
                #     break
                # length = a1 - a0
                # # read line number
                # ln = int.from_bytes(f.read(2), 'little')
                data = f.read(length) # skip newline
                m = [str(ln), ' ']
                in_quotes = False
                number = -1
                i = 0
                while i < len(data):
                    b = data[i]
                    i += 1
                    print('reading char:',hex(b))
                    if (b == 0x0d):
                        break
                    if int(b) == ord('"'):
                        in_quotes = not in_quotes
                    #used_map = self.invOrd if in_quotes else self.invTokens
                    if in_quotes:
                        m.append(chr(self.codeToChar.get(b, b)))
                    else:
                        if b in self.invTokens:
                            m.append(self.invTokens[b])
                            m.append(' ')
                        else:
                            character =chr(self.codeToChar.get(b, b))
                            if number == -1 and (character.isdigit() or character == '.'):
                                print('start number')
                                number = 0
                            elif number == 0 and not (character.isdigit() or character=='.'):
                                print('end number')
                                number=-1
                                i+=5
                                continue
                            m.append(character)
                inst = ''.join(m)
                print(inst)
                li[ln] = inst
                #a =input("Procedi?")
        return li
    def save(self, lines: list, file: str):
        #print (' --- save not specified for zx-spectrum')
        print(' -- saving file: ', file)
        fn = Path(file).stem

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
        data = bytearray()
        # --- header
        header_length = 19
        data += header_length.to_bytes(2, 'little')
        data.append(0)
        data.append(0)
        fn = fn[:10].ljust(10)
        data.extend(map(ord, fn))
        astart = 32768
        data += total_length.to_bytes(2, 'little')
        data += astart.to_bytes(2, 'little')
        data += total_length.to_bytes(2, 'little')
        # checksum
        data.append(self.checksum(data[2:]))
        # --- basic program
        data += (total_length + 2).to_bytes(2, 'little')
        basic_start_index = len(data)
        data.append(0xFF)
        for s in sorted_instructions:
            data += instructions[s]
        # --- basic program checksum
        data.append(self.checksum(data[basic_start_index:]))
        with open(file, 'wb') as f:
            f.write(data)
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
                instruction.append(self.charToCode.get(ord(s[i]), ord(s[i])))
                i += 1
                continue
            else:
                if s[i] in self.verbatim_start_chars:
                    verbatim = True
                    verbatim_end_char = self.verbatim_start_chars[s[i]]
                    instruction.append(self.charToCode.get(ord(s[i]), ord(s[i])))
                    i += 1
                    continue
            start = i
            token = -1
            node = self.tokenRoot
            while i < len(s):
                #if s[i].isspace():
                #    i += 1
                #    continue
                cc = s[i].upper()
                print('try',cc)
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
                print('token not found starting @ ',start, s[start])
                if not current_number and s[start].isdigit():
                    print('start number @ ', s[start])
                    current_number = [s[start]]
                elif current_number:
                    if s[start].isdigit() or s[start] == '.':
                        current_number.append(s[start])
                    else:
                        instruction.append(0x0E)
                        instruction += self.convertNumber(''.join(current_number))
                        current_number = None
                # don't append space
                if not s[start].isspace():
                    instruction.append(self.charToCode.get(ord(s[start]), ord(s[start])))
                i = start + 1
            #    i += 1
        if current_number:
            instruction.append(0x0E)
            instruction += self.convertNumber(''.join(current_number))
        instruction.append(0x0D)
        return instruction