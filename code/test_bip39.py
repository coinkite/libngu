#!/bin/sh
# 
try:
    # make the test data
    from mnemonic import Mnemonic

    eng = Mnemonic('english')

    with open('b39-data.txt', 'wt') as fd:
        for ln in [16, 20, 24, 28, 32]:
            for val in [b'\0', b'\xff', b'\xab\xcd', b'\xa5\xa5', b'\xAA', b'\x55']:
                vector = val * (ln // len(val))
                exp = eng.to_mnemonic(vector)
                print('(%r, %r)' % (vector, exp), file=fd)

except:
    pass

import bip39

def test_b2a():

    # run the test
    for ln in open('b39-data.txt', 'rt').readlines():
        #print(ln)
        vector, expect = eval(ln)

        ans = bip39.b2a_words(vector)
        assert ans == expect, "(got) %r != (expected) %r " % (ans, expect)

def test_a2b():
    for ln in open('b39-data.txt', 'rt').readlines():
        value, words = eval(ln)
        got = bip39.a2b_words(words)
        assert got == value

def test_guessing():
    for ln in open('b39-data.txt', 'rt').readlines():
        value, words = eval(ln)
        words = words.split()
        maybe = bip39.a2b_words_guess(words[:-1])
        assert words[-1] in maybe, '%r not in %r' % (words[-1], maybe)

def test_prefix():

    assert bip39.next_char('act') == (True, 'ioru')
    assert bip39.next_char('dkfjh') == (False, '')
    assert bip39.next_char('a') == (False, 'bcdefghilmnprstuvwx')
    assert bip39.next_char('q') == (False, 'u')
    assert bip39.next_char('qu') == (False, 'aeio')
    assert bip39.next_char('present') == (True, '')
    assert bip39.next_char('zoo') == (True, '')
    assert bip39.next_char('zo') == (False, 'no')
    


test_b2a()
test_prefix()
test_a2b()
test_guessing()

print('PASS')
