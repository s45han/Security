from collections import Counter
from operator import itemgetter

### ===================================
# get ciphertext when provided plaintext&key
# get key when provided cipher and plaintext
def encrypt_singles(txt,key,decrypt):
    #decrypt=-1, encrypt=1
    cipher_num=alphabet_shifts.index(txt)+decrypt*alphabet_shifts.index(key)
    return alphabet_shifts[cipher_num%26]
 
 ### ===================================   
#initialization
ciphertext = open("ciphertext_cher","r").read()
LOOP_TIMES=100
i=1
key_size=1
e_frequency=0.12702
max_frequency=0
most_likely_key_size=1

init_alphabet={
    "a":0,
    "b":0,
    "c":0,
    "d":0,
    "e":0,
    "f":0,
    "g":0,
    "h":0,
    "i":0,
    "j":0,
    "k":0,
    "l":0,
    "m":0,
    "n":0,
    "o":0,
    "p":0,
    "q":0,
    "r":0,
    "s":0,
    "t":0,
    "u":0,
    "v":0,
    "w":0,
    "x":0,
    "y":0,
    "z":0,

}

alphabet_shifts=["a","b","c","d","e","f","g","h","i","j","k","l","m",
"n","o","p","q","r","s","t","u","v","w","x","y","z"]

grouped_cipher={}
sorted_cipher={}
possible_pairs={}
possible_keysize=[]

### ===================================
### finding key length
while i<=LOOP_TIMES: #try different key length
    
    for group_num in range(0,key_size):
        grouped_cipher[group_num]=""
        sorted_cipher[group_num]=init_alphabet.copy()
    
    index=0
    while index<len(ciphertext):
        
        for group_num in range(0,key_size):
            letter=ciphertext[index]
            grouped_cipher[group_num]+=letter
            sorted_cipher[group_num][letter]+=1
            
            index+=1
            if index>=len(ciphertext):
                break

    i+=1

    # frequency analysis for each group
    # print("key length: "+str(key_size))
    
    analyzed_letter={}
    max_cur_frequency=0
    for group_num in range(0,key_size):

        total_length=len(grouped_cipher[group_num])        
        analyzed_letter[group_num]={}

        for letter in sorted_cipher[group_num]:
            frequency= sorted_cipher[group_num][letter]*1.0/(total_length)                       
            analyzed_letter[group_num][letter]=frequency
            
            max_cur_frequency=max(max_cur_frequency,frequency)           
            
        analyzed_letter[group_num]=sorted(analyzed_letter[group_num].items(),key=itemgetter(1), reverse=True)
        # print analyzed_letter
    
    # If the max frequency is close to freq of e of 12.702%    
    if abs(max_cur_frequency-e_frequency)<=0.01 and max_cur_frequency>=max_frequency :#and most_likely_key_size==key_size: #close to e's frequency
        possible_pairs[key_size]=analyzed_letter
        # print(key_size,max_cur_frequency)
        possible_keysize.append(key_size)
        # print analyzed_letter
    
    
    key_size+=1
print possible_keysize

### ===================================
### determining the most likely keysize
max_common=0
for size1 in possible_keysize:
    common=0
    for size2 in possible_keysize:
        if  size1!=size2 and size2%size1==0 :
            common+=1
    if max(max_common,common)==common:
        max_common=common
        most_likely_key_size=size1

print("--> Most likely key size: %s" % most_likely_key_size)


### ===================================
### getting key after knowing most likely key length through looping each group
keys=""
# csv=

for group_num in range(0,most_likely_key_size):
    print("\n--> Statistics of letter at index %d every %d loops: " % (group_num,most_likely_key_size))
    print(possible_pairs[most_likely_key_size][group_num])
    letter=possible_pairs[most_likely_key_size][group_num][0][0]
    frequency=possible_pairs[most_likely_key_size][group_num][0][1]    
    key=encrypt_singles(letter,"e",decrypt=-1)

    print ("%s , %f --> %s" %(letter,frequency,key))
    keys+=key
print("\n--> Keys: "+ keys)

### ===================================
### decrypt entire cipher text
index=0
plaintext=""
while index<len(ciphertext):
    plaintext+=encrypt_singles(ciphertext[index],keys[index%most_likely_key_size],decrypt=-1)
    index+=1


### ===================================
### store to file
file=open("plaintext.txt","w")
file.write(plaintext)
file.close()
print("\nOriginal text stored to plaintext.txt")