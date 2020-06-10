####  FINAL VERSION ####

# Authors:
   # Antonin DUDRAGNE #
   # Alexandre CORNET #
   # Matthieu LECOMTE #

# Imports
from Vigenere_attack import vigenere_crack

# Declaration of dedicated alphabet
lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
special_char = dict(àâÀ="a", éèêÉÈ="e", ùûÙ="u", çÇ="c", î='i', ôÔ='o')
numbers = "0123456789"
ponctuation = "!?:;.,'-’"

# French data base for statistic attack:
statistic_french_base_c = [7.11, 1.14, 3.18, 3.67, 12.10, 1.11, 1.23, 1.11, 6.59, 0.34, 0.29, 4.96, 2.62, 6.39, 5.02, 2.49, 0.65, 6.07,6.51, 5.92, 4.49, 1.11, 0.17, 0.38, 0.46, 0.15]


####################################################
####            Interface Function              ####
####################################################
             
def user_interface():
    # Main menu
    print("======  Main menu   ", "="*34)
    print("1 Cesar methods")
    print("2 Vigenere methods")
    print("3 Beaufort methods")
    print("4 Quit")
    print("="*55)
    cmd = int(input(">>> "))
    if cmd == 1:
        cesar_interface()
    elif cmd == 2:
        vigenere_interface()
    elif cmd == 3:
        beaufort_interface()
    elif cmd == 4:
        print("See you soon")

# Interface for cesar encryption
def cesar_interface():
    #Display the menu
    print("=" * 55)
    print("1 Crypt", "              Crypt a message ")
    print("2 Uncrypt", "            Uncrypt a message")
    print("3 Bruteforce", "         Attack with brute force")
    print("4 Crypto Analysis", "    Attack with statistic method")
    print("5 Return to main menu")
    print("6 Quit")
    print("=" * 55)
    while 1:
        cmd = int(input(">>> "))
        if cmd == 1:
            infos = ask("cesar", "crypt")
            print("Crypted message: ", cesar_encrypt(infos[0], infos[1]))
        elif cmd == 2:
            infos = ask("cesar", "decrypt")
            print("Decrypted message: ", cesar_decrypt(infos[0], infos[1]))
        elif cmd == 3:
            infos = ask("cesar", "bf")
            cesar_bf(infos)
        elif cmd == 4:
            infos = ask("cesar", "ana")
            crypto_analyse_stats(infos, 5)
        elif cmd == 5:
            user_interface()
            break
        elif cmd == 6:
            print("See you soon")
            break
        else:
            print("Invalid command")
            continue
 
# Interface for vigenere encryption
def vigenere_interface():  
    # Display the menu on console
    print("="*55)
    print("1 Crypt")
    print("2 Uncrypt")
    print("3 Crack Vigenere (beta test)")
    print("4 Return to main menu")
    print("5 Quit")
    print("="*55)
    while 1:
        cmd = int(input(">>> "))
        if cmd == 1:
            infos = ask("v", "crypt")
            print("Crypted message: ", vigenere_encrypt(infos[0], infos[1]))
        elif cmd == 2:
            infos = ask("v", "decrypt")
            print("Decrypted message: ", vigenere_decrypt(infos[0], infos[1]))
        elif cmd == 3:
            info = ask("v", "analysis")
            key = vigenere_crack(info)
            print("The key was: ", key)
            print("Decrypted message: ", vigenere_decrypt(info, key))
        elif cmd == 4:
            user_interface()
            break
        elif cmd == 5:
            print("See you soon")
            break
        else:
            print("Invalid command")
            continue

# Interface for Beaufort encryption
def beaufort_interface():
    print("=" * 55)
    print("1 Crypt")
    print("2 Uncrypt")
    print("3 Return to main menu")
    print("4 Quit")
    print("=" * 55)
    while 1:
        cmd = int(input(">>> "))
        if cmd == 1:
            infos = ask("v", "crypt")
            print("Crypted message: ", vigenere_decrypt(infos[0], infos[1]))  # We've just inverted the two method of vigenere in order to compute Beaufort's ones
        elif cmd == 2:
            infos = ask("v", "decrypt")
            print("Decrypted message: ", vigenere_encrypt(infos[0], infos[1]))
        elif cmd == 3:
            user_interface()
            break
        elif cmd == 4:
            print("See you soon :)")
            break
        else:
            print("Invalid command")

# Input method  
def ask(method, type):
    # Input: method(string) -> it identifies rather cesar method or an other
    #        type(string) -> identifies crypting, decrypting and analysis
    while 1:
        if method == "cesar":
            if type == "crypt" or type == "decrypt":
                message = input("Text: ")
                key = input("Key: ")
                try:
                    key = int(key)
                    if not 0 < key < 26:
                        print("La clé doit être comprise entre 0 et 25")
                        continue
                    return message, key
                except ValueError:
                    print("La clé doit être comprise entre 0 et 25")
                    continue
            else:
                message = input("Crypted text: ")
                return message
        else:
            if type == "crypt" or type == "decrypt":
                message = input("Text: ")
                key = input("Key: ")
                cmpt = 0
                for letter in key:
                    if letter in lowercase:
                        cmpt += 1
                    elif letter in uppercase:
                        cmpt += 1
                if cmpt == len(key):
                    return message, key
                else:
                    print("La clé doit être composée de lettres de l'alphabet")
                    continue
            else:
                message = input("Crypted text: ")
                return message


###############################################
####        Cesar encryption methods       ####
###############################################

def cesar_encrypt(chain, key):
    # Receive chain(string) = string to encrypt
    # Receive key(int) = key with which "chain" will be encrypt
    # Output = "crypted_message"(string)
    crypted_message = ''

    for char in chain:
        if char in lowercase:
            new_index = (lowercase.index(char) + key) % 26
            crypted_message += lowercase[new_index]
        elif char in uppercase:
            new_index = (uppercase.index(char) + key) % 26
            crypted_message += uppercase[new_index]
        elif char in numbers:
            new_index = (numbers.index(char) + key) % 10
            crypted_message += numbers[new_index]
        else:
            ok = False
            for chain in special_char.keys():
                if char in chain:
                    new_index = (lowercase.index(special_char[chain]) + key) % 26
                    crypted_message += lowercase[new_index]
                    ok = not ok
            if not ok:
                crypted_message += char

    return crypted_message


def cesar_decrypt(chain, key):
    # Receive chain(string) = string to decrypt
    # Receive key(int) = key with which "chain" will be decrypt
    # Output = "decrypted_message"(string)
    decrypted_message = ''

    for char in chain:
        if char in lowercase:
            new_index = (lowercase.index(char) - key) % 26
            decrypted_message += lowercase[new_index]
        elif char in uppercase:
            new_index = (uppercase.index(char) - key) % 26
            decrypted_message += uppercase[new_index]
        elif char in numbers:
            new_index = (numbers.index(char) - key) % 10
            decrypted_message += numbers[new_index]
        else:
            decrypted_message += char
    return decrypted_message

def cesar_bf(chain):
    # Receive chain(string) = string to attack
    for i in range(1, 26):
        decrypted_message = cesar_decrypt(chain, i)
        print(decrypted_message, "    the key of encryption was: {0}".format(i))
        


###################################################
####        Vigenere encryption methods        ####
###################################################

def vigenere_encrypt(chain, key):
    # Receive chain(string) = string to encrypt
    # Receive key(string) = key with which "chain" will be encrypt
    # Output = "crypted_message"(string)
    cmpt = 0               # Set a var in order to know where we are in the key
    crypted_message = ''
    key = key.lower()      # We don't want uppercase in key -> it's easier

    for letters in chain:
        if letters in lowercase:
            number = (lowercase.index(letters) + lowercase.index(key[cmpt])) % 26
            crypted_message += lowercase[number]
            cmpt = (cmpt + 1) % len(key)
        elif letters in uppercase:
            number = (uppercase.index(letters) + lowercase.index(key[cmpt])) % 26
            crypted_message += uppercase[number]
            cmpt = (cmpt + 1) % len(key)
        else:
            ok = False
            for string in special_char.keys():
                if letters in string:
                    number = (lowercase.index(special_char[string]) + lowercase.index(key[cmpt])) % 26
                    crypted_message += lowercase[number]
                    cmpt = (cmpt + 1) % len(key)
                    ok = not ok
            if not ok:
                crypted_message += letters

    return crypted_message

def vigenere_decrypt(chain, key):
    # Receive chain(string) = string to decrypt
    # Receive key(string) = key with which "chain" will be decrypt
    # Output = "decrypted_message"(string)
    cmpt = 0
    decrypted_message = ''
    key = key.lower()

    for letters in chain:
        if letters in lowercase:
            number = (lowercase.index(letters) - lowercase.index(key[cmpt])) % 26
            decrypted_message += lowercase[number]
            cmpt = (cmpt + 1) % len(key)
        elif letters in uppercase:
            number = (uppercase.index(letters) - lowercase.index(key[cmpt])) % 26
            decrypted_message += uppercase[number]
            cmpt = (cmpt + 1) % len(key)
        else:
            decrypted_message += letters

    return decrypted_message


###################################################
####         Cryptanalyse statistique           ###
###################################################

def crypto_analyse_stats(chain, error):
    # Input: chain(string) -> message we have to analyse
    #        error(int) -> give the precision of the suggestion algorithm
    # Output: built table in console with 4 rows (Charactère, Effectif, Fréquence et Suggestion)

    #Declaration of the base we will use
    base = statistic_french_base_c

    #Transform character into lowercase
    chain = chain.lower()

    #Creation of work table (statistic table)
    work_table = [["Charactères"], \
                  ["Effectifs  "], \
                  ["Fréquences "], \
                  ["Suggestion "]]
    total_effectif = 0

    #  Statistic Analysis  #
    for char in chain:
        if work_table[0].count(char) == 0:
            if char != ' ' and not char in ponctuation:
                work_table[0].append(char)
                work_table[1].append(1)
        else:
            index = work_table[0].index(char)
            work_table[1][index] += 1
            total_effectif += 1
    #Computing frequences (via total effectif)
    for number in work_table[1]:
        if type(number) is not str:
            work_table[2].append(round((number / total_effectif) * 100, 2))

    # Sort of the "worktable"  characteres in order to save only those which are in "lowercase"

    for char in work_table[0]:
        if not char == "Charactères" and not char in lowercase:
            work_table[0].remove(char)

    #Compare with data base # return the value of database that fit the best to computing frequences, if there is not: return 'NA'
    maxi_proche = [0, 'NA']   #Save var to choose the best char (see below)
    for index in range(1, len(work_table[0])):
        for base_i in range(len(base)):
            if base[base_i] - error < work_table[2][index] < base[base_i] + error:    #testing if frequence value is in range
                rapport = work_table[2][index]/base[base_i]    #Compute how close the two values are
                sugested_char = lowercase[base_i]
                if maxi_proche[0] < rapport:  # If precedent save quotient is smaller, redefine the suggested char value
                    maxi_proche[1] = sugested_char
                maxi_proche[0] = max(maxi_proche[0], rapport)
        work_table[3].append(maxi_proche[1])
        maxi_proche = [0, 'NA']

    # Display work_table with a clean print table
    for i in range(4):
        for j in range(len(work_table[0])):
            char = work_table[i][j]
            if type(char) is str:
                lenght = len(char)
                if lenght < 5:
                    char += ' ' * (5 - lenght)
            elif type(char) is int or type(char) is float:
                char = str(char)
                lenght = len(char)
                if lenght < 5:
                    char += ' ' * (5 - lenght)
            print("|", char, end='')
        print('||')
    print('')

    # Print the suggested message based only with the pic (we considered that the pic correspond to the 'e')
    work_table[1].remove("Effectifs  ")  #Because for the following instruction str in not supported
    pic = work_table[1].index(max(work_table[1]))
    pic_index = lowercase.index(work_table[0][pic+1])
    e_index = lowercase.index('e')
    if e_index <= pic_index:
        decalage = pic_index - e_index
        print("Suggested message (based only on {0} frequence):".format(work_table[0][pic+1]), cesar_decrypt(chain, decalage), "   The key was:", decalage)
    else:
        decalage = 26 - e_index + pic_index
        print("Suggested message (based only on {0} frequence):".format(work_table[0][pic+1]), cesar_decrypt(chain, decalage), "   The key was:", decalage)

# Run
user_interface()