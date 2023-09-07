import matplotlib.pyplot as plt
import numpy as np
import os

def word_checker(crypt, words):
    if len(crypt) != 0:
        word_match_per = 0
        for word in crypt:
            if word in words:
                word_match_per += 1
        word_match_per = (word_match_per / len(crypt)) * 100
        return word_match_per
    return 0

def push_letters(inp, letters, lim = 1000, push_by = 1): 
    proccessed_inp = []
    forming_word = ""
    out = ""
    for letter in inp:   
        if len(forming_word) >= 25: forming_word == ""
        try: 
            forming_word += letters[(letters.index(letter)+push_by)%len(letters)]
            out += forming_word[-1]
        except Exception:     
            out += letter
            if letter == " " or letter == "\n": 
                proccessed_inp.append(forming_word)
                forming_word = ""
        if len(proccessed_inp) > lim:
            return out, proccessed_inp
    if len(proccessed_inp) <= lim:
        proccessed_inp.append(forming_word)
    return out, proccessed_inp

def letter_push(letters, lim, words, pass_min_val, crypt):
    mod_crypt = crypt
    for j in range(26):
        mod_crypt, parsed_crypt = push_letters(mod_crypt, letters, lim)
        per = word_checker(parsed_crypt, words)
        parsed_crypt = []
        if per >= pass_min_val:
            input(f"Crypt may have been decoded! Letters were shifted by {j+1}.")
            unecrypted_txt, _ = push_letters(crypt, letters, push_by=(j+1))
            input(f"\n\n{unecrypted_txt}")
            if input("\nHas it been decrypted (y/n) ").lower() == "y": return unecrypted_txt
        else: 
            print(f"Letter shift by {j+1} failed!")
            print(f"Crypt became ({crypt})\n\n")
    input("\n\nLetter shift failed!")
    os.system("cls")
    return False

def decrypt():
    pass_min_val = 50
    lim = 50

    crypt = ""
    t = []

    letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    letters_frequency_norm = [8.2, 1.5, 2.8,4.3,12.7,2.2,2,6.1,7,0.15,0.77,4,2.4,6.7,7.5,1.9,0.095,6,6.3,9.1,2.8,0.98,2.4,0.15,2,0.074]
    letters_frequency_crypt = []
    c_len = 0

    while True:
        code = input("Enter the crypt (the more the better) type 'done' when done: ").lower() + "\n"
        if code == "done\n":
            break
        t.append(code)   

    for i, z in enumerate(t):
        crypt += z

    crypt = crypt[:-1]

    for i, letter in enumerate(letters):
        z = crypt.count(letter)
        letters_frequency_crypt.append(z)
        c_len += z

    for i, _ in enumerate(letters):
        letters_frequency_crypt[i] = (letters_frequency_crypt[i] / c_len) * 100

    x = letters
    y1, y2 = letters_frequency_crypt, letters_frequency_norm

    for i in range(52):
        if i <= 1:
            if i % 2 == 0:
                plt.bar(x[i//2], y2[i//2], color = "blue", label = "Expected Statistics")
            else: 
                plt.bar(x[i//2].upper(), y1[i//2], color = "red", label = "Crypt's Statistics")
                #plt.bar(str(i), 0)
        else:
            if i % 2 == 0:
                plt.bar(x[i//2], y2[i//2], color = "blue")
            else: 
                plt.bar(x[i//2].upper(), y1[i//2], color = "red")
                #plt.bar(str(i), 0)

    with open(r"D:\Productivity\Programming\GenericProgrammingLanguages\Python\Programs\Other\Calculator\words.txt", encoding="utf8") as f:
        x = f.readlines()
    words = []

    plt.legend(loc="upper left")
    plt.title("Difference in letter counts of the 'crypt' and the 'expected'")
    plt.xlabel("Letters")
    plt.ylabel("Percentage of Occurence")
    plt.show()

    for w in x: 
        words.append(w[:-1].lower())

    if not letter_push(letters, lim, words, pass_min_val, crypt):
        pass

decrypt()