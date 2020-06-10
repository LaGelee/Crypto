##################################
####      Vigenere Attack     ####
##################################

# Declaration of dedicated variable
# Alphabet
lowercase = "abcdefghijklmnopqrstuvwxyz"


statistic_french_base_c = [7.11, 1.14, 3.18, 3.67, 12.10, 1.11, 1.23, 1.11, 6.59, 0.34, 0.29, 4.96, 2.62, 6.39, 5.02, 2.49, 0.65, 6.07,6.51, 5.92, 4.49, 1.11, 0.17, 0.38, 0.46, 0.15]
prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
espected_IC = 0.074

def vigenere_crack(chain=str):
    # Input: "chain"(string) -> It is the Vigenere coded message
    # Outputs: "Key"(string) -> key with which the message hes been coded

    Key = ''
    
    # Sort the char of Vigenere sequences in order to save only those which belong to "lowercase"
    chain = chain.lower()
    sorted_chain = ''
    for char in chain:
        if char in lowercase:
            sorted_chain = sorted_chain + char

    ##  Search for repeted sequences  ##

    # Algorythm that remark the repetition of the text and compute their distance
    repeated_chain = [[], []]  # Var which will save the repeated chains and their distances
    max_length = 6      # Set the max length of a repeated chain
    min_length = 3     # Set the min length of a repeated chain
    n_value = 4          # Set the number of value we want per length
    for length in range(min_length, max_length+1): # Do the process for all size of sequences
        count = 0
        for x in range(len(sorted_chain)):
            if count >= n_value:
                break
            if x+length < len(sorted_chain):
                tampon_chain = ''.join(sorted_chain[x+b] for b in range(length))
                if repeated_chain[0].count(tampon_chain) != 0:
                    continue
            else:
                break
            for i in range(x+length, len(sorted_chain)):
                if count >= n_value:
                    break
                if i+length < len(sorted_chain):
                    tested_chain = ''.join(sorted_chain[i+b] for b in range(length))
                    if tested_chain == tampon_chain:
                        distance = abs(i - x)
                        repeated_chain[0].append(tampon_chain)
                        repeated_chain[1].append(distance)
                        count += 1
                else:
                    break 

    if len(repeated_chain[0]) == 0:
        return "Pas de répétition, on ne peut pas décoder ce message..."

    ## Search for the length of the key  ##
    factor_list_rough = []
    maximum = [0, 0, 0]
    # Computing all possible factor
    for distance in range(len(repeated_chain[1])):
        factor = decompose(repeated_chain[1][distance])
        basic_len = len(factor)
        for number_index in range(basic_len):
            for number_index2 in range(basic_len):
                if number_index != number_index2:
                    new_factor = factor[number_index] * factor[number_index2]
                    if factor.count(new_factor) == 0:
                        factor.append(new_factor)
        sort(factor)
        for number in factor:
            factor_list_rough.append(number)

    # Finding length of the key
    for factors in range(len(factor_list_rough)):  
        number = factor_list_rough[factors]
        if factor_list_rough.count(number) > maximum[0]:
            maximum = [factor_list_rough.count(number), factors, number]
        elif factor_list_rough.count(number) == maximum[0]:
            better_factor = optimization_with_IC(sorted_chain, [number, maximum[2]])
            if better_factor != maximum[2]:
                maximum = [factor_list_rough.count(number), factors, number]

    length_key = factor_list_rough[maximum[1]]
    
    for x in range(length_key):
        treated_chain = ''.join(sorted_chain[x+b*length_key] for b in range(int(len(sorted_chain)/length_key)-1)) # Generate the text from index x and then x + b*length (every step = length of the key)
        saved_frequences = [[], []]
        for char in treated_chain:
            if saved_frequences[0].count(char) == 0:
                saved_frequences[0].append(char)
                saved_frequences[1].append(treated_chain.count(char))
        print("Only for debug:", saved_frequences)  #Only for debug if it is needed
        index_string = saved_frequences[1].index(max(saved_frequences[1]))
        max_char = saved_frequences[0][index_string]
        if lowercase.index(max_char) >= lowercase.index('e'):
            index = lowercase.index(max_char) - lowercase.index('e')
            Key += (lowercase[index])
        else:
            index = 26 - lowercase.index('e') + lowercase.index(max_char)
            Key += (lowercase[index])
    return Key
        

# Method that decompose an integer into prime numbers
def decompose(n=int):
    # Input: "n"(int) -> Number we want to decompose
    # Output: "decomposed_n"(list) -> Return all the prime number of the decomposition
    diviseur_index = 0
    decomposed_n = []
    count = 0
    while n > 1:
        if count == 100:
            decomposed_n.append(n)
            return decomposed_n
        number = prime_numbers[diviseur_index]
        if n % number == 0:
            decomposed_n.append(number)
            n = n/number
        if diviseur_index < len(prime_numbers) - 1:
            diviseur_index += 1
        else:
            diviseur_index = 0
        count += 1
    return decomposed_n

# Method that sort of the table in order to prevent from repetition of values
def sort(table):
    # Input: "table"(list) -> List we want to sort
    # Output: "table"(list) -> List without same values
    for things in table:
        if table.count(things) > 0:
            while table.count(things) > 1:
                table.remove(things)
    return table

# Method call only if needed
# It allows to choose the factor that is the closest of the IC for french (the best of two equal frequenced factor)
def optimization_with_IC(chain, doubt):  # This fonction allows us to choose between prime number or multiple
    # chain(string) -> analysed chain
    # doubt(list) -> list of all factors we have a doubt on
    best_IC = []
    for nfactor in range(len(doubt)):
        size = doubt[nfactor]
        if size < len(chain)/size:
            treated_chain = ''.join(chain[b*size] for b in range(int(len(chain)/size)))
        else:
            continue
        n = len(treated_chain)
        IC = sum(((treated_chain.count(lowercase[x]) - 1 )*treated_chain.count(lowercase[x]) / (n * (n - 1)) for x in range(26)))
        best_IC.append(IC / espected_IC)
    if len(best_IC) > 0:
        return doubt[best_IC.index(max(best_IC))]
    else:
        return 0