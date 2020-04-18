main.py frequency --input_file "Alice.txt" --output_file "frequencies_file.txt"

main.py encode --input_file "Alice.txt" --output_file "encode_file.txt" --cipher caesar --key 7

main.py decode --input_file "encode_file.txt" --output_file "copy_Alice.txt" --cipher caesar --key 7

main.py break --input_file "encode_file.txt" --output_file "hacked_Alice.txt" --frequency_file "frequencies_file.txt"

main.py decode --key CpluspLuSisFine --cipher vigenere
>> RnebgcTmLpwGmfx
<< PythonIsTheBest

main.py encode --key CpluspLuSisFine --cipher vigenere
>> PythonIsTheBest
<< RnebgcTmLpwGmfx
