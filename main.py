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
    diction = collections.Counter()
    for iterator in range(len(string_of_alphabet)):
        diction[string_of_alphabet[iterator]] = iterator
        diction[iterator] = string_of_alphabet[iterator]
    diction['size'] = len(string_of_alphabet)
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


def encode_caesar(key_of_code, encrypted_string):
    return code_caesar(key_of_code, encrypted_string)


def decode_caesar(key_of_code, encrypted_string):
    return code_caesar(-key_of_code, encrypted_string)


def code_caesar(key_of_code, encrypted_string):
    answer_string = ""
    for iterator in encrypted_string:
        encrypted = False
        for type_of_alphabet in ALPHABET:
            if iterator in type_of_alphabet:
                answer_string += type_of_alphabet[
                    (type_of_alphabet[iterator] +
                     key_of_code % type_of_alphabet['size'] +
                     type_of_alphabet['size']) % type_of_alphabet['size']
                    ]
                encrypted = True
                break
        if not encrypted:
            answer_string += iterator
    return answer_string


'''
////////////
Cipher Vigenere
////////////
'''


def encode_vigenere(key_of_code, encrypted_string):
    return code_vigenere(1, key_of_code, encrypted_string)


def decode_vigenere(key_of_code, encrypted_string):
    return code_vigenere(-1, key_of_code, encrypted_string)


def code_vigenere(coefficient, key_of_code, encrypted_string):
    answer_string = ""
    for iterator in range(len(encrypted_string)):
        encrypting = False
        for type_of_enc in ALPHABET:
            if encrypted_string[iterator] in type_of_enc:
                for type_of_key in ALPHABET:
                    if key_of_code[iterator % len(key_of_code)] in type_of_key:
                        answer_string += type_of_enc[
                            (type_of_enc[encrypted_string[iterator]] +
                             (coefficient * type_of_key[key_of_code[
                                 iterator % len(key_of_code)]])
                             % type_of_enc['size'] + type_of_enc['size']) %
                            type_of_enc['size']
                        ]
                        encrypting = True
                        break
                break
        if not encrypting:
            answer_string += encrypted_string[iterator]
    return answer_string


'''
//////////////
Cipher Vernam
//////////////
'''


def encode_vernam(key_of_code, encrypted_string):
    answer_string = ""
    for iterator in range(len(encrypted_string)):
        encrypting = False
        for type_of_enc in ALPHABET:
            if encrypted_string[iterator] in type_of_enc:
                for type_of_key in ALPHABET:
                    if key_of_code[iterator] in type_of_key:
                        answer_string += type_of_enc[
                            type_of_enc[encrypted_string[iterator]] ^
                            type_of_key[key_of_code[iterator %
                                                    len(key_of_code)]]
                        ]
                        encrypting = True
                        break
                break
        if not encrypting:
            answer_string += encrypted_string[iterator]
    return answer_string


def decode_vernam(key_of_code, encrypted_string):
    return encode_vernam(key_of_code, encrypted_string)


'''
////////////
Calculate Frequency
////////////
'''


def frequency_calculator_string(frequency_string):
    counter = collections.Counter()
    for iterator in frequency_string:
        if iterator in LOWERCASE:
            counter[iterator] += 1
        if iterator in UPPERCASE:
            counter[LOWERCASE[UPPERCASE[iterator]]] += 1
    return counter


def frequency_calculator_text(frequency_text):
    counter = collections.Counter()
    for iterator in frequency_text:
        counter += frequency_calculator_string(iterator)
    return counter


'''
////////////
Breaking
////////////
'''


def mse(list1, list2):
    answer = 0
    for iterator in range(len(list1)):
        answer += (list1[iterator] - list2[iterator]) ** 2
    return answer


def breaking_key(key_counter, text):
    counter_list = []
    for iterator in range(LOWERCASE['size']):
        counter_list.append(key_counter[LOWERCASE[iterator]])

    calculator = frequency_calculator_text(text)
    mse_key_list = list()
    for hacked_key in range(LOWERCASE['size']):
        calculating_list = []
        for iterator in range(LOWERCASE['size']):
            calculating_list.append(
                calculator[LOWERCASE[(hacked_key + iterator)
                                     % LOWERCASE['size']]]
            )
        mse_key_list.append(
            (mse(counter_list, calculating_list), hacked_key)
        )
    return sorted(mse_key_list)[0][1]


'''
////////////
Pair of Tools
////////////
'''

any_input = False
any_output = False
fin = None
fout = None
input_filename = ""
output_filename = ""


def write_text(*strings):
    for iterator in strings:
        if any_output:
            fout.write(str(iterator))
        else:
            print(iterator, end="")


def encode_in_shape(code_shape, key_of_code, encrypted_string):
    if code_shape == 'caesar':
        return encode_caesar(int(key_of_code), encrypted_string)
    elif code_shape == 'vigenere':
        return encode_vigenere(key_of_code, encrypted_string)
    elif code_shape == 'vernam':
        return encode_vernam(key_of_code, encrypted_string)


def decode_in_shape(code_shape, key_of_code, encrypted_string):
    if code_shape == 'caesar':
        return decode_caesar(int(key_of_code), encrypted_string)
    elif code_shape == 'vigenere':
        return decode_vigenere(key_of_code, encrypted_string)
    elif code_shape == 'vernam':
        return decode_vernam(key_of_code, encrypted_string)


def encode(args):
    if args.input_file is not None:
        for line in fin:
            write_text(encode_in_shape(args.cipher, args.key, line))
    else:
        lines = sys.stdin.readlines()
        for line in lines:
            write_text(encode_in_shape(args.cipher, args.key, line))


def decode(args):
    if args.input_file is not None:
        for line in fin:
            write_text(decode_in_shape(args.cipher, args.key, line))
    else:
        lines = sys.stdin.readlines()
        for line in lines:
            write_text(decode_in_shape(args.cipher, args.key, line))


def frequency(args):
    json.dump(frequency_calculator_text(fin), fout)


def hack(args):
    freq_counter = json.load(open(args.frequencies, 'r'))
    k = breaking_key(freq_counter, fin)
    copy = open(input_filename, 'r')
    for it in copy:
        write_text(decode_in_shape('caesar', k, it))


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
parser_encode = subparsers.add_parser('encode', help=' encode command ')
parser_encode.set_defaults(mode='encode', function=encode)
parser_encode.add_argument(
    '--cipher', choices=['caesar', 'vigenere', 'vernam'],
    help=" type of cipher ", required=True
)
parser_encode.add_argument('--key', help=" key of cipher ", required=True)
parser_encode.add_argument('--input_file', help=" input file ")
parser_encode.add_argument('--output_file', help=" output file ")


parser_decode = subparsers.add_parser('decode', help=' decode command')
parser_decode.set_defaults(mode='decode', function=decode)
parser_decode.add_argument(
    '--cipher', choices=['caesar', 'vigenere', 'vernam'],
    help=' type o cipher ', required=True
)
parser_decode.add_argument('--key', help='Cipher key', required=True)
parser_decode.add_argument('--input_file', help=' input file ')
parser_decode.add_argument('--output_file', help=' output file ')


parser_freq = subparsers.add_parser('frequency', help=' frequency command')
parser_freq.set_defaults(mode='frequency', function=frequency)
parser_freq.add_argument('--input_file', help=' input file ')
parser_freq.add_argument('--output_file', help=' model file', required=True)


parser_hack = subparsers.add_parser('break', help=' hack command ')
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
    any_input = True
    input_filename = commands.input_file


if commands.output_file is not None:
    fout = open(commands.output_file, 'w')
    any_output = True
    output_filename = commands.output_file

commands.function(commands)
