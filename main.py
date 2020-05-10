import string
import collections
import argparse
import json
import sys

'''
////////////
Constants
////////////
'''


def built_alphabet(string_of_alphabet):
    diction = dict()
    for ind, symbol in enumerate(string_of_alphabet):
        diction[symbol] = ind
    diction['size'] = len(string_of_alphabet)
    diction['base'] = string_of_alphabet
    return diction


LOWERCASE = built_alphabet(string.ascii_lowercase)
UPPERCASE = built_alphabet(string.ascii_uppercase)
DIGITS = built_alphabet(string.digits)

ALPHABET = [LOWERCASE, UPPERCASE, DIGITS]

'''
////////////
Cipher Caesar
////////////
'''


def caesar(mode, key_of_code, encode_string):
    if mode == 'encode':
        return encode_caesar(key_of_code, encode_string)
    return decode_caesar(key_of_code, encode_string)


def encode_caesar(key_of_code, encode_string):
    return code_caesar(key_of_code, encode_string)


def decode_caesar(key_of_code, decode_string):
    return code_caesar(-key_of_code, decode_string)


def code_caesar_symbol(key_of_code, code_symbol):
    for code_type in ALPHABET:
        if code_symbol in code_type:
            return code_type['base'][
                (code_type[code_symbol] + key_of_code) % code_type['size']
            ]
    return code_symbol


def code_caesar(key_of_code, code_string):
    answer_string = ""
    for symbol in code_string:
        answer_string += code_caesar_symbol(key_of_code, symbol)
    return answer_string


'''
////////////
Cipher Vigenere
////////////
'''


def vigenere(mode, key_of_code, encode_string):
    if mode == 'encode':
        return encode_vigenere(key_of_code, encode_string)
    return decode_vigenere(key_of_code, encode_string)


def encode_vigenere(key_of_code, encode_string):
    return code_vigenere(1, key_of_code, encode_string)


def decode_vigenere(key_of_code, decode_string):
    return code_vigenere(-1, key_of_code, decode_string)


def code_vigenere_symbol(coefficient, key_symbol, code_symbol):
    for code_type in ALPHABET:
        if code_symbol in code_type:
            for key_type in ALPHABET:
                if key_symbol in key_type:
                    return code_type['base'][
                        (code_type[code_symbol] + coefficient *
                         key_type[key_symbol]) % code_type['size']
                    ]
            return code_symbol
    return code_symbol


def code_vigenere(coefficient, key_of_code, code_string):
    answer_string = ""
    for ind, symbol in enumerate(code_string):
        answer_string += code_vigenere_symbol(
            coefficient, key_of_code[ind % len(key_of_code)], symbol
        )
    return answer_string


'''
//////////////
Cipher Vernam
//////////////
'''


def vernam(mode, key_of_code, encode_string):
    if mode == 'encode':
        return encode_vernam(key_of_code, encode_string)
    return decode_vernam(key_of_code, encode_string)


def code_vernam_symbol(key_symbol, code_symbol):
    for code_type in ALPHABET:
        if code_symbol in code_type:
            for key_type in ALPHABET:
                if key_symbol in key_type:
                    return code_type['base'][
                        (code_type[code_symbol] ^ key_type[key_symbol])
                    ]
            return code_symbol
    return code_symbol


def encode_vernam(key_of_code, encode_string):
    answer_string = ""
    for ind, symbol in enumerate(encode_string):
        answer_string += code_vernam_symbol(
            key_of_code[ind % len(key_of_code)], symbol
        )
    return answer_string


decode_vernam = encode_vernam

'''
////////////
Calculate Frequency
////////////
'''


def string_frequency_calculate(frequency_string):
    return collections.Counter(
        [char for char in frequency_string.lower() if char in LOWERCASE]
    )


def text_frequency_calculate(frequency_text):
    result = collections.Counter()
    for line in frequency_text:
        result += string_frequency_calculate(line)

    return result


'''
////////////
Breaking
////////////
'''


def mse(list1, list2):
    return sum((elem1-elem2) ** 2 for elem1, elem2 in zip(list1, list2))


def breaking_key(key_counter, text):
    counter_list = [key_counter[symbol] for symbol in string.ascii_lowercase]

    calculator = text_frequency_calculate(text)
    mse_key_list = list()
    for hack_key in range(LOWERCASE['size']):
        calculating_list = [
            calculator[string.ascii_lowercase[i % LOWERCASE['size']]]
            for i in range(hack_key, hack_key + LOWERCASE['size'])
        ]
        mse_key_list.append(
            (mse(counter_list, calculating_list), hack_key)
        )
    return min(mse_key_list)[1]


'''
////////////
Pair of Tools
////////////
'''

any_output = False
fin = None
fout = None
input_filename = ""


def write_text(*lines):
    for line in lines:
        if any_output:
            fout.write(line)
        else:
            print(line, end="")


def code_in_shape(code_shape, mode, key_of_code, encode_string):
    if code_shape == 'caesar':
        return caesar(mode, int(key_of_code), encode_string)
    elif code_shape == 'vigenere':
        return vigenere(mode, key_of_code, encode_string)
    elif code_shape == 'vernam':
        return vernam(mode, key_of_code, encode_string)


def encode_decode(command):
    for line in fin:
        write_text(
            code_in_shape(command.cipher, command.mode, command.key, line)
        )


def frequency(command):
    json.dump(text_frequency_calculate(fin), fout)


def hack(command):
    with open(commands.frequencies, 'r') as frequencies:
        freq_counter = json.load(frequencies)
        k = breaking_key(freq_counter, fin)
        with open(input_filename, 'r') as copy:
            for it in copy:
                write_text(code_in_shape('caesar', 'decode', k, it))


'''
////////////
Console
////////////
'''


parser = argparse.ArgumentParser(
    description=" Command line arguments reader",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
subparsers = parser.add_subparsers()
parser_encode = subparsers.add_parser('encode', help=' for encoding text ')
parser_encode.set_defaults(mode='encode', function=encode_decode)
parser_encode.add_argument(
    '--cipher', choices=['caesar', 'vigenere', 'vernam'],
    help=" type of cipher ", required=True
)
parser_encode.add_argument('--key', required=True,
                           help=" number(for caesar) or word(for else) ")
parser_encode.add_argument('--input_file', help=" input file ")
parser_encode.add_argument('--output_file', help=" output file ")


parser_decode = subparsers.add_parser('decode', help=' for decoding text ')
parser_decode.set_defaults(mode='decode', function=encode_decode)
parser_decode.add_argument(
    '--cipher', choices=['caesar', 'vigenere', 'vernam'],
    help=' type o cipher ', required=True
)
parser_decode.add_argument('--key', required=True,
                           help=" number(for caesar) or word(for else) ")
parser_decode.add_argument('--input_file', help=' input file ')
parser_decode.add_argument('--output_file', help=' output file ')


parser_freq = subparsers.add_parser('frequency',
                                    help=' for counting frequency ')
parser_freq.set_defaults(mode='frequency', function=frequency)
parser_freq.add_argument('--input_file', help=' input file ')
parser_freq.add_argument('--output_file', help=' model file', required=True)


parser_hack = subparsers.add_parser('break', help=' for hacking text ')
parser_hack.set_defaults(mode='break', function=hack)
parser_hack.add_argument(
    '--cipher', choices=['caesar'], help=' type of cipher ', default='caesar'
)
parser_hack.add_argument('--input_file', help=' input file ')
parser_hack.add_argument('--output_file', help=' output file ')
parser_hack.add_argument('--frequencies', help=' model file ', required=True)

commands = parser.parse_args()

if commands.input_file is not None:
    fin = open(commands.input_file, 'r')
    input_filename = commands.input_file
else:
    fin = sys.stdin.readlines()


if commands.output_file is not None:
    fout = open(commands.output_file, 'w')
    any_output = True

commands.function(commands)
