import string
import collections
import argparse

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
        if iterator >= len(key_of_code):
            answer_string += encrypted_string[iterator]
            continue
        encrypting = False
        for type_of_enc in ALPHABET:
            if encrypted_string[iterator] in type_of_enc:
                for type_of_key in ALPHABET:
                    if key_of_code[iterator] in type_of_key:
                        answer_string += type_of_enc[
                            (type_of_enc[encrypted_string[iterator]] +
                             (coefficient * type_of_key[key_of_code[iterator]])
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
        if iterator >= len(key_of_code):
            answer_string += encrypted_string[iterator]
            continue
        encrypting = False
        for type_of_enc in ALPHABET:
            if encrypted_string[iterator] in type_of_enc:
                for type_of_key in ALPHABET:
                    if key_of_code[iterator] in type_of_key:
                        answer_string += type_of_enc[
                            type_of_enc[encrypted_string[iterator]] ^
                            type_of_key[key_of_code[iterator]]
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


def write_text(*strings):
    for iterator in strings:
        if any_output_direction:
            fout.write(str(iterator))
        else:
            print(iterator)


def encode(code_shape, key_of_code, encrypted_string):
    if code_shape == 'caesar':
        return encode_caesar(int(key_of_code), encrypted_string)
    elif code_shape == 'vigenere':
        return encode_vigenere(key_of_code, encrypted_string)
    elif code_shape == 'vernam':
        return encode_vernam(key_of_code, encrypted_string)


def decode(code_shape, key_of_code, encrypted_string):
    if code_shape == 'caesar':
        return decode_caesar(int(key_of_code), encrypted_string)
    elif code_shape == 'vigenere':
        return decode_vigenere(key_of_code, encrypted_string)
    elif code_shape == 'vernam':
        return decode_vernam(key_of_code, encrypted_string)


'''
////////////
Console
////////////
'''


commands = argparse.ArgumentParser()
commands.add_argument('command', help='encode|decode|frequency|break')
commands.add_argument('--cipher', help='caesar|vigenere')
commands.add_argument('--key', help='key == number|word')
commands.add_argument('--input_file', help='file with text to do something')
commands.add_argument('--output_file', help='the output file')
commands.add_argument('--frequencies', help='file with frequencies')
args = commands.parse_args()


if args.input_file is not None:
    fin = open(args.input_file, 'r')
    any_input_direction = True
    input_filename = args.input_file
else:
    any_input_direction = False
    input_filename = "file.nothing"


if args.output_file is not None:
    fout = open(args.output_file, 'w')
    any_output_direction = True
    output_filename = args.output_file
else:
    any_output_direction = False
    output_filename = "file.nothing"


if args.command == 'encode':
    if any_input_direction:
        for line in fin:
            write_text(encode(args.cipher, args.key, line))
    else:
        EOF = True
        while EOF:
            try:
                line = input()
                write_text(encode(args.cipher, args.key, line))
            except EOFError:
                EOF = False
                pass
elif args.command == 'decode':
    if any_input_direction:
        for line in fin:
            write_text(decode(args.cipher, args.key, line))
    else:
        EOF = True
        while EOF:
            try:
                line = input()
                write_text(decode(args.cipher, args.key, line))
            except EOFError:
                EOF = False
                pass
elif args.command == 'frequency':
    ans = frequency_calculator_text(fin)
    for key, value in ans.items():
        write_text("{}: {}".format(key, value))
elif args.command == 'break':
    frequencies = open(args.frequencies, 'r')
    freq_counter = collections.Counter()
    for freq in frequencies:
        freq_counter[freq[0]] = int(freq.split(' ')[1])
    k = breaking_key(freq_counter, fin)
    copy = open(input_filename, 'r')
    for it in copy:
        write_text(decode('caesar', k, it))


