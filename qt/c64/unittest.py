#!/usr/bin/python3

from tokenizer import SpeccyTokenizer


def zx_number(t: SpeccyTokenizer, s: str, result):
    a = t.convertNumber(s)
    b = ["{:02x}".format(x) for x in a]
    print(b)
    


def test1():
    s = SpeccyTokenizer('systems/zx-spectrum/token.yaml')
    zx_number(s, '1.5', [])

test1()