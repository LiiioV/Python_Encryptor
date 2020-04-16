import string
import collections


'''
////////////
Tools
////////////
'''


def built_alphabet(strr):
    diction = dict()
    for it in range(len(strr)):
        diction[strr[it]] = it
        diction[it] = strr[it]
    diction['size'] = len(strr)
    return diction


lowercase = built_alphabet(string.ascii_lowercase)
uppercase = built_alphabet(string.ascii_uppercase)
digits = built_alphabet(string.digits)
punctations = built_alphabet(string.punctuation + ' ')

alphabet = [lowercase, uppercase, digits, punctations]


'''
////////////
Cipher Caesar
////////////
'''


def encode_caesar(key, uncode_str):
    return code_caesar(key, uncode_str)


def decode_caesar(key, uncode_str):
    return code_caesar(-key, uncode_str)


def code_caesar(key, uncode_str):
    ans = ""
    for it in uncode_str:
        for typee in alphabet:
            if it in typee:
                ans += typee[(typee[it] + key % typee['size']
                              + typee['size']) % typee['size']]
                break
    return ans


'''
////////////
Cipher Vigenere
////////////
'''


def encode_vigenere(key, uncode_str):
    return code_vigenere(1, key, uncode_str)


def decode_vigenere(key, uncode_str):
    return code_vigenere(-1, key, uncode_str)


def code_vigenere(coef, key, uncode_str):
    ans = ""
    for it in range(len(uncode_str)):
        for typee in alphabet:
            if uncode_str[it] in typee:
                ans += typee[(typee[uncode_str[it]] + coef * typee[key[it]]
                              + typee['size']) % typee['size']]
                break
    return ans


'''
////////////
Calculate Frequency
////////////
'''


def freq_calc_str(freq_str):
    c = collections.Counter()
    for it in freq_str:
        if it in lowercase:
            c[it] += 1
        if it in uppercase:
            c[lowercase[uppercase[it]]] += 1
    return c


def freq_calc_text(*freq_strs):
    c = collections.Counter()
    for it in freq_strs:
        c += freq_calc_str(it)
    return c


'''
////////////
Breaking
////////////
'''


def mse(list1, list2):
    ans = 0
    for it in range(len(list1)):
        ans += (list1[it] - list2[it])**2
    return ans


def breaking_key(counter, *strs):
    counter_list = []
    for it in range(lowercase['size']):
        counter_list.append(counter[lowercase[it]])

    calc = freq_calc_text(*strs)
    mse_key_list = list()
    for key in range(lowercase['size']):
        calc_list = []
        for it in range(lowercase['size']):
            calc_list.append(calc[lowercase[(key + it) % lowercase['size']]])
        mse_key_list.append((mse(counter_list, calc_list), key))
    return sorted(mse_key_list)[0][1]


'''
////////////
Pair of Tools
////////////
'''


def write_str(*args):
    for it in args:
        if out:
            fout.write(str(it))
            fout.write('\n')
        else:
            print(it)


def encode(code_shape, code_key, uncode_str):
    if code_shape == 'caesar':
        return encode_caesar(int(code_key), uncode_str)
    elif code_shape == 'vigenere':
        return encode_vigenere(code_key, uncode_str)


def decode(code_shape, code_key, uncode_str):
    if code_shape == 'caesar':
        return decode_caesar(int(code_key), uncode_str)
    elif code_shape == 'vigenere':
        return decode_vigenere(code_key, uncode_str)


'''
////////////
Console
////////////
'''

inp = False
out = False


input_string = input().split("--")
for it in input_string:
    if it[0] == 'i':
        inp = True
        input_file = it.split(' ')[1]
        fin = open(it.split(' ')[1], 'r')
    elif it[0] == 'o':
        out = True
        fout = open(it.split(" ")[1], 'w')
    elif it[0] == 'c':
        shape = it.split(" ")[1]
    elif it[0] == 'k':
        key = it.split(" ")[1]
    else:
        func = it.split(' ')[0]


if func == 'encode':
    if inp:
        for it in fin:
            write_str(encode(shape, key, it))
    else:
        while True:
            try:
                s = input()
                write_str(encode(shape, key, s))
            except:
                break
elif func == 'decode':
    if inp:
        for it in fin:
            write_str(decode(shape, key, it))
    else:
        while True:
            try:
                s = input()
                write_str(decode(shape, key, s))
            except:
                break
elif func == 'frequency':
    ans = freq_calc_text(*fin)
    for key, value in ans.items():
        write_str("{}: {}".format(key, value))
elif func == 'breaking':
    file_frequency = open(key, 'r')
    freq_counter = collections.Counter()
    for it in file_frequency:
        freq_counter[it[0]] = int(it.split(' ')[1])
    k = breaking_key(freq_counter, *fin)
    copy = open(input_file, 'r')
    for it in copy:
        write_str(decode('caesar', k, it))


'''
decode --input enc.txt --output dec.txt --key 1 --cipher caesar
encode --input Alice.txt --output enc.txt --key 1 --cipher caesar
encode --input newf.txt --output bb.txt --key 1 --cipher caesar
decode --input bb.txt --output aa.txt --key 1 --cipher caesar
frequency --input Alice.txt --output out.txt
breaking --input enc.txt --output break.txt --key out.txt
'''