from tokenizer import ITokenizer

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
