# This MONSTROSTIY was made by Sachit
# Considering the code quality, not sure if I should be proud or ashamed

try:
  import matplotlib.pyplot as plt
  import os
  import pyperclip
  import time
except ModuleNotFoundError:
  input("You haven't downloaded all the modules!\nYou will have to follow these steps to fix this.\n(press enter)")
  input("1) Open the 'command prompt' (just search for it on your computer).")
  input("2) Type these snippets of code into it:")
  input("\tpip install matplotlib")
  input("\tpip install pyperclip")
  input("You should now be good to go. (Close this window and re-run the program)")

LET_FREQ_NORM = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2, 6.1, 7, 0.15, 0.77, 4, 2.4, 6.7, 7.5, 1.9, 0.095, 6, 6.3, 9.1, 2.8, 0.98, 2.4, 0.15, 2, 0.074]
LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"  ]
PATH = "\\".join(os.path.abspath(__file__).split("\\")[:-1]) + "\\"
#NAME = input("Gimme a SOLID name: ")
NAME = "TEST"

TOP_WRD_CNT = 15

PASS_MIN_VAL = 50
LIM = 50

with open(PATH+r"all_WORDS.txt",encoding="utf8") as f:
  x = f.readlines()
WORDS = []
for w in x:
  WORDS.append(w[:-1].lower())

#########

def initialise():
  #try:
  #  with open(f"{PATH}\\Ciphers\\{NAME}.txt", "w"):  pass
  #except OSError: 
  #  raise Exception("The name was NOT solid.")
  
  temp = []
  crypt = ""

  while True:
    code = input(
        "Enter the crypt (the more the better) type 'done' when done: ").lower(
        ) + "\n"
    if code == "done\n":
      break
    temp.append(code)


  for z in temp:
    crypt += z
  return crypt[:-1]

def let_freq_ana(letters_frequency_crypt):
  x = LETTERS
  y1, y2 = letters_frequency_crypt, LET_FREQ_NORM

  for i in range(52):
    if i <= 1:
      if i % 2 == 0:
        plt.bar(x[i // 2], y2[i // 2], color="blue", label="Expected Statistics")
      else:
        plt.bar(x[i // 2].upper(), y1[i // 2], color="red", label="Crypt's Statistics")
        #plt.bar(str(i), 0)
    else:
      if i % 2 == 0:
        plt.bar(x[i // 2], y2[i // 2], color="blue")
      else:
        plt.bar(x[i // 2].upper(), y1[i // 2], color="red")
        #plt.bar(str(i), 0)

  print(f"\n\n{letters_frequency_crypt}")
  pyperclip.copy(str(letters_frequency_crypt))

  plt.legend(loc="upper left")
  plt.title("Difference in letter counts of the 'crypt' and the 'expected'")
  plt.xlabel("LETTERS")
  plt.ylabel("Percentage of Occurence")
  plt.show()

def word_freq_ana(crypt):
  crypt_words = {}
  crypt = crypt.split(" ")
  for crypt_word in crypt:
    prev_occurences = 0
    try:
      prev_occurences = crypt_words[crypt_word]
    except KeyError:
      pass
    crypt_words[crypt_word] = 1 + prev_occurences

  top = sorted(crypt_words.items(), key=lambda x:x[1], reverse=True)
  print(f"\n\n{dict(top)}")
  pyperclip.copy(str(dict(top)))

  top = top[:TOP_WRD_CNT]
  freq = []
  crypt_words = []

  for pair in top:
    crypt_words.append(pair[0])
    freq.append(pair[1])

  plt.bar(crypt_words, freq)
  plt.legend(loc="upper left")
  plt.title(f"Frequency of the top {TOP_WRD_CNT} words.")
  plt.xlabel("Words")
  plt.ylabel("Frequency of occurence")
  plt.show()

  print(crypt_words, freq)

def word_checker(crypt):
  if len(crypt) != 0:
    word_match_per = 0
    for word in crypt:
      if word in WORDS:
        word_match_per += 1
    word_match_per = (word_match_per / len(crypt)) * 100
  if word_match_per >= PASS_MIN_VAL:
    print("Cipher may have been cracked...")
    time.sleep(0.1)
    print(f"\n\nThe crypt became \n-->\n{" ".join(crypt)}\n-->")
    inp = input("Has the crypt been solved (y/n)? ")
    if inp.lower() == "y": return True
    else: return False

def push_LETTERS(inp: str, push_by=1, lim = LIM):
  proccessed_inp = []
  forming_word = ""
  out = ""
  for letter in inp:
    if len(forming_word) >= 25: forming_word = ""
    try:
      forming_word += LETTERS[(LETTERS.index(letter) + push_by) % len(LETTERS)]
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

def sub_lets(crypt: str, let_dict: dict):
  decrypted_str = ""
  for let in crypt[:min(LIM, len(crypt))]:
    try:
      decrypted_str += let_dict[let.lower()]
    except KeyError:
      decrypted_str += let
  return decrypted_str

def letter_push(crypt):
  mod_crypt = crypt
  for j in range(26):
    mod_crypt, parsed_crypt = push_LETTERS(mod_crypt)
    passed = word_checker(parsed_crypt)
    parsed_crypt = []
    if passed:
      return (j+1)
    else:
      print(f"Letter shift by {j+1} failed!")
      print(f"Crypt became ({mod_crypt})\n\n")
  input("\n\nLetter shift failed!")
  os.system("cls")
  return -1

def un_sub(inp, key, sort_by_freq = False, lim = LIM) -> str:
  by_freq = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z']
  ret_str = ""
  for letter in inp[:min(len(inp), lim)]:
    try:
      if sort_by_freq: 
        ret_str += by_freq[key.index(letter.lower())-1]
      else: ret_str += key[LETTERS.index(letter.lower())]
    except ValueError:
      ret_str += letter
  return ret_str

def decipher_sub(crypt, let_freq_cy):
  t = sorted({let: freq for let, freq in zip(LETTERS, let_freq_cy)}.items(), reverse = True, key = lambda x:x[1])
  t = dict(t).keys()
  let_freq_cy = list(t)
  ret = un_sub(crypt, let_freq_cy, True, 9999999999999)
  passed = word_checker(ret.split(" "))
  if not passed:
    print("Sub cipher (CURRENTLY IN PROGRESS - UNRELIABLE) has failed.\nThis is what we got\n")
  return ret

def anagram(crypt):
  order = input("What order are the letters in for the anagram?\n[Input should be given in a form akin to '162435'. If the word is more than 10 letters long, add a leading 0 for the numbers under 10.]\n>>> ")
  crypt_magnitude = (len(crypt[0]) // 10)+1
  order = [int(order[i:i+crypt_magnitude])-1 for i in range(0, len(order), crypt_magnitude)]
  words = ""
  for word in crypt.split(" "):
    temp = ["" for _ in range(len(word))]
    for i, seq in enumerate(order):
      temp[i] = word[seq]
    words += "".join(temp)
  return words

def decrypt():
  letters_frequency_crypt = [0 for _ in range(26)]
  c_len = 0
  crypt = initialise()

  for i, letter in enumerate(LETTERS):
    z = crypt.count(letter)
    letters_frequency_crypt[i] = z
    c_len += z

  for i in range(26):
    letters_frequency_crypt[i] = (letters_frequency_crypt[i] / c_len) * 100

  inp = input(f"What do you want to do?\n1) Run letter and word analysis\n2) Try and solve the cipher independently\n3) Anagram helper\n")
  if inp == "1":
    let_freq_ana(letters_frequency_crypt)
    word_freq_ana(crypt)
  elif inp == "2":
    push = letter_push(crypt)
    if push >= 0:
      print(f"\n\n{push_LETTERS(crypt, push, 99999999999)[0]}")
      return 0
    print(decipher_sub(crypt, letters_frequency_crypt))
  elif inp == "3": 
    print(anagram(crypt))
    
decrypt()
input("")
#key = ["q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"]
#key = ["z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y"]
#print(un_sub("Hello my name is sachit sharma, how are you?", key))