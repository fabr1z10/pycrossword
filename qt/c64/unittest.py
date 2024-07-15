#!/usr/bin/python3

from tokenizer import SpeccyTokenizer


def zx_number(t: SpeccyTokenizer, s: str, result):
    a = t.convertNumber(s)
    b = ["{:02x}".format(x) for x in a]
    print('number:', s, ' --> ', b, a == bytearray(result))
    


def test1():
    s = SpeccyTokenizer('systems/zx-spectrum/token.yaml')
    # zx_number(s, '1.5', [0x81, 0x40, 0x00, 0x00, 0x00])
    # zx_number(s, '0.5', [0x80, 0x00, 0x00, 0x00, 0x00])
    # zx_number(s, '42', [0x00, 0x00, 0x2a, 0x00, 0x00])
    # zx_number(s, '1024', [0x00, 0x00, 0x00, 0x04, 0x00])
    zx_number(s, '0.3', [0x7f, 0x19, 0x99, 0x99, 0x9a])
    zx_number(s, '0.0001', [0x73, 0x51, 0xb7, 0x17, 0x59])

test1()