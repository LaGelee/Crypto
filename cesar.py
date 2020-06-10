#Author: Yuxuama

#Declaration of dedicated alphabet

lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
special_char = "!?:;.,'-êéèàçù"
numbers = "0123456789"

#French data base for statistic attack

statistic_french_base = [['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'], \
                         [7.11, 1.14, 3.18, 3.67, 12.10, 1.11, 1.23, 1.11, 6.59, 0.34, 0.29, 4.96, 2.62, 6.39, 5.02, 2.49, 0.65, 6.07, \
                          6.51, 5.92, 4.49, 1.11, 0.17, 0.38, 0.46, 0.15]]

## Asking fonction ## Two mode 'c' for encryption and 'd' for decryption

def ask(for_what):
    while 1:
        if for_what == 'c':
            try:
                key = int(input("Donne une clé de codage: "))
                message = input("Donne le message que tu veux crypter: ")
                if not 0 < key < 26:
                    print("La clé de codage doit être un chiffre entre 1 et 25")
                    continue
                return message, key
                break
            except ValueError:
                print("La clé de codage doit être un chiffre entre 1 et 25")
                continue
        elif for_what == 'd':
            try:
                key = int(input("Donne une clé de décodage: "))
                message = input("Donne le message que tu veux décrypter: ")
                if not 0 < key < 26:
                    print("La clé de codage doit être un chiffre entre 1 et 25")
                    continue
                return message, key
                break
            except ValueError:
                print("La clé de codage doit être un chiffre entre 1 et 25")
                continue

##  Encoding a message with Cesar process  ##

def cesar_encrypt(chain, key):
    crypted_message = ''

    #Crypt th message
    for char in chain:
        if char in lowercase:
            new_index = (lowercase.index(char) + key) % 26
            crypted_message += lowercase[new_index]
        elif char in uppercase:
            new_index = (uppercase.index(char) + key) % 26
            crypted_message += uppercase[new_index]
        elif char in special_char:
            new_index = (special_char.index(char) + key) % 14
            crypted_message += special_char[new_index]
        elif char in numbers:
            new_index = (numbers.index(char) + key) % 10
            crypted_message += numbers[new_index]
        else:
            crypted_message += char
    return crypted_message


def cesar_uncrypt(chain, key):
    decrypted_message = ''
    for char in chain:
        if char in lowercase:
            new_indew = (lowercase.index(char) - key) % 26
            decrypted_message += lowercase[new_indew]
        elif char in uppercase:
            new_indew = (uppercase.index(char) - key) % 26
            decrypted_message += uppercase[new_indew]
        elif char in special_char:
            new_indew = (special_char.index(char) - key) % 14
            decrypted_message += special_char[new_indew]
        elif char in numbers:
            new_indew = (numbers.index(char) - key) % 10
            decrypted_message += numbers[new_indew]
        else:
            decrypted_message += char
    return decrypted_message

## Computation of all solution for a given coded chain ##

def cesar_bf(chain):
    decrypted_message = ''
    for i in range(1, 26):
        decrypted_message = cesar_uncrypt(chain, i)
        print(decrypted_message, "    the key of encryption was: {0}".format(i))


## Cryptography statistic analysis ##

def cesar_cs(chain, error):
    #Transform character into lowercase
    chain = chain.lower()

    #Creation of work table (statistic table)
    work_table = [["Charactères"], \
                  ["Effectifs  "], \
                  ["Fréquence  "], \
                  ["Suggestion "]]
    total_effectif = 0

    #  Statistic Analysis  #
    for char in chain:
        if work_table[0].count(char) == 0:
            if char != ' ' and not char in special_char:
                work_table[0].append(char)
                work_table[1].append(1)
        else:
            index = work_table[0].index(char)
            work_table[1][index] += 1
    #Computing frequences (via total effectif)
    for i in range(2):
        for number in work_table[1]:
            if type(number) is not str:
                if i == 0:
                    total_effectif += number
                else:
                    work_table[2].append(round((number / total_effectif) * 100, 2))

    #Compare with data base #return the value of database that fit the well to computing frequences, if there is not: return 'NA'
    base = statistic_french_base
    maxi_proche = [0, 'NA']   #Save var to chose the best char (see below)
    for index in range(1, len(work_table[0])):
        for base_i in range(len(base[0])):
            if base[1][base_i] - error < work_table[2][index] < base[1][base_i] + error:    #testing if frequence value is in range
                rapport = work_table[2][index]/base[1][base_i]    #Compute how close the two values are
                sugested_char = base[0][base_i]
                if maxi_proche[0] < rapport:  #If precedent save quotient is smaller, redefine the suggested char value
                    maxi_proche[1] = sugested_char
                maxi_proche[0] = max(maxi_proche[0], rapport)
        work_table[3].append(maxi_proche[1])
        maxi_proche = [0, 'NA']

    #Display work_table with a clean print table
    for i in range(4):
        for j in range(len(work_table[0])):
            char = work_table[i][j]
            if type(char) is str:
                lenght = len(char)
                if lenght < 6:
                    char += ' '*(6-lenght)
            elif type(char) is int or type(char) is float:
                char = str(char)
                lenght = len(char)
                if lenght < 6:
                    char += ' ' * (6 - lenght)
            print("|", char, end='')
        print('||')




#Display of the menu
print("=" * 60)
print("1 Crypt", "             Crypt a message ")
print("2 Uncrypt", "           Uncrypt a message")
print("3 Bruteforce", "        Attack with brute force")
print("4 Crypto Analysis", "   Attack with statistic method")
print("5 Quit")
print("=" * 60)

#Ask to user what he wants to do couple until he quits
while 1:
    try:
        print(" ")
        will = int(input(">>> "))
    except ValueError:
        print("Tu dois rentrer un chiffre entre 1 et 5")
        continue
    if will == 1:
        answer = ask('c')
        print(" ")
        print("======  Encoded message   ", "="*45)
        print(cesar_encrypt(answer[0], answer[1]))
        print("="*72)
    elif will == 2:
        answer = ask('d')
        print(" ")
        print("======  Decoded message  ", "="*50)
        print(cesar_uncrypt(answer[0], answer[1]))
        print("=" * 72)
    elif will == 3:
        message = input("Quel message veux tu attaquer en brute force: ")
        print(" ")
        print("======  Decoded solution  ", "="*50)
        cesar_bf(message)
    elif will == 4:
        message = input("Quel message veux tu attaquer en cryptanalyse statistique: ")
        print(" ")
        print("======  Crypto Analysis   ", "="*45)
        cesar_cs(message, 1)
    elif will == 5:
        print("See you soon")
        break
    else:
        print("Commande invalide, tu dois rentrer un nombre entre 1 et 5")
