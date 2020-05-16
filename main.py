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
    alphabet_dict = {
        symbol: ind for ind, symbol in enumerate(string_of_alphabet)
    }
    alphabet_dict['size'] = len(string_of_alphabet)
    alphabet_dict['alphabet_string'] = string_of_alphabet
    return alphabet_dict


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
            return code_type['alphabet_string'][
                (code_type[code_symbol] + key_of_code) % code_type['size']
            ]
    return code_symbol


def code_caesar(key_of_code, code_string):
    return ''.join(code_caesar_symbol(key_of_code, symbol)
                   for symbol in code_string)


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
                    return code_type['alphabet_string'][
                        (code_type[code_symbol] + coefficient *
                         key_type[key_symbol]) % code_type['size']
                    ]
            return code_symbol
    return code_symbol


def code_vigenere(coefficient, key_of_code, code_string):
    return ''.join(code_vigenere_symbol(coefficient, key_of_code, symbol)
                   for symbol in code_string)


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
                    return code_type['alphabet_string'][
                        code_type[code_symbol] ^ key_type[key_symbol]
                    ]
            return code_symbol
    return code_symbol


def encode_vernam(key_of_code, encode_string):
    return ''.join(code_vernam_symbol(key_of_code, symbol)
                   for symbol in encode_string)


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


def find_mse(list1, list2):
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
            (find_mse(counter_list, calculating_list), hack_key)
        )
    return min(mse_key_list)[1]


'''
////////////
Pair of Tools
////////////
'''


def get_input_text(path):
    if path is None:
        return sys.stdin.readlines()
    else:
        with open(path, 'r') as input_file:
            return input_file.readlines()


def get_output_file(path):
    if path is None:
        return None
    else:
        return open(path, 'w')


def write_text(*lines, fout):
    for line in lines:
        if fout is not None:
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
    fin = get_input_text(command.input_file)
    fout = get_output_file(command.output_file)
    for line in fin:
        write_text(
            code_in_shape(command.cipher, command.mode, command.key, line),
            fout=fout
        )


def frequency(command):
    fout = get_output_file(command.output_file)
    json.dump(text_frequency_calculate(
        get_input_text(command.input_file)), fp=fout
    )


def hack(command):
    with open(command.frequencies, 'r') as frequencies:
        freq_counter = json.load(frequencies)
        fin = get_input_text(command.input_file)
        fout = get_output_file(command.output_file)
        key = breaking_key(freq_counter, fin)

        for line in fin:
            write_text(
                code_in_shape('caesar', 'decode', key, line),
                fout=fout
            )


'''
////////////
Console
////////////
'''


def parse_args():
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
    parser_encode.add_argument(
        '--key', required=True, help=" number(for caesar) or word(for else) "
    )
    parser_encode.add_argument(
        '--input_file', help=" path to the file to be encrypted "
                               )
    parser_encode.add_argument(
        '--output_file', help=' path to the file to be write result '
    )

    parser_decode = subparsers.add_parser('decode', help=' for decoding text ')
    parser_decode.set_defaults(mode='decode', function=encode_decode)
    parser_decode.add_argument(
        '--cipher', choices=['caesar', 'vigenere', 'vernam'],
        help=' type o cipher ', required=True
    )
    parser_decode.add_argument(
        '--key', required=True, help=" number(for caesar) or word(for else) "
    )
    parser_decode.add_argument(
        '--input_file', help=' path to the file to be encrypted '
    )
    parser_decode.add_argument(
        '--output_file', help=' path to the file to be write result '
    )

    parser_freq = subparsers.add_parser('frequency',
                                        help=' for counting frequency ')
    parser_freq.set_defaults(mode='frequency', function=frequency)
    parser_freq.add_argument(
        '--input_file', help=' path to the file to calculate frequency '
    )
    parser_freq.add_argument(
        '--output_file', help=' path to the file to be write result ',
        required=True
    )

    parser_hack = subparsers.add_parser('break', help=' for hacking text ')
    parser_hack.set_defaults(mode='break', function=hack)
    parser_hack.add_argument(
        '--cipher', choices=['caesar'], help=' type of cipher ',
        default='caesar'
    )
    parser_hack.add_argument('--input_file', help=' path to the file to hack ')
    parser_hack.add_argument(
        '--output_file', help=' path to the file to be write result '
    )
    parser_hack.add_argument(
        '--frequencies', help=' path to the file with frequencies ',
        required=True
    )
    return parser.parse_args()


def main():
    args = parse_args()
    args.function(args)


if __name__ == '__main__':
    main()
