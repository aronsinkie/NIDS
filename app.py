import re
import sys
import nltk
import string
import difflib
from  io import StringIO
from colorama import Fore, Style
from flask import Flask, render_template, request, jsonify
from spellcheckersql import create_database, is_word_in_dictionary,read_prefixes_from_database,read_VC_dictionary
app = Flask(__name__)
RIBI,am=read_VC_dictionary()

noun_list=[]
verb_list=[]
adjective_list=[]
amharic_verb_prefixes = read_prefixes_from_database('verb_prefix')
amharic_verb_suffixes = read_prefixes_from_database('verb_sufix')
amharic_noun_prefixes = read_prefixes_from_database('noun_prefix')
amharic_noun_suffixes = read_prefixes_from_database('noun_sufix')
amharic_adj_prefixes = read_prefixes_from_database('adj_prefix')
amharic_adj_suffixes  = read_prefixes_from_database('adj_sufix')
noun_list=read_prefixes_from_database('noun_list')
verb_list=read_prefixes_from_database('verb_list')
adj_list=read_prefixes_from_database('adj_list')
root_list=read_prefixes_from_database('root')

def so_called_steam_noun_word(word):
    for prefix in amharic_noun_prefixes:
        if word.startswith(prefix):
            word = word[len(prefix):]
            break
    for suffix in amharic_noun_suffixes:
        if word.endswith(suffix):
            word = word[:-len(suffix)]
            break
        word = word.replace("-", "")
    return word

def so_called_steam_verb_word(word):
    for prefix in amharic_verb_prefixes:
        if word.startswith(prefix):
            word = word[len(prefix):]
            break
    for suffix in amharic_verb_suffixes:
        if word.endswith(suffix):
            word = word[:-len(suffix)]
            break
        word = word.replace("-", "")
    return word

def so_called_steam_adj_word(word):
    for prefix in amharic_adj_prefixes:
        if word.startswith(prefix):
            word = word[len(prefix):]
            break
    for suffix in amharic_adj_suffixes:
        if word.endswith(suffix):
            word = word[:-len(suffix)]
            break
        word = word.replace("-", "")
    return word

def Erbata_TIGBERA(KAL: str, RIBI: dict) -> str:
    Anababi_Erbata = [RIBI.get(FIDEL, '') for FIDEL in KAL]
    Anababi_Erbata = '-'.join(Anababi_Erbata)
    return Anababi_Erbata
def reverse_Erbata(KAL: str, RIBI: dict) -> str:
    if KAL is None:
        return None
    else: 
        split_words = KAL.split("-")
        new_word = ''
        for split_word in split_words: 
            for key, value in RIBI.items():  
                if value == split_word: 
                    new_word += key
                    break
                else:
                     new_word += split_word
                     new_word += '-'
    return new_word.rstrip('-')

def add_amharic_noun_affixes(stem_word):
    words_with_affixes = []

    for prefix in amharic_noun_prefixes:
        words_with_affixes.append(prefix + stem_word)

    for suffix in amharic_noun_suffixes:
        words_with_affixes.append(stem_word[:-1] + suffix)

    return words_with_affixes
def add_amharic_verb_affixes(stem_word):
    words_with_affixes = []

    for prefix in amharic_verb_prefixes:
        words_with_affixes.append(prefix + stem_word)

    for suffix in amharic_verb_suffixes:
        words_with_affixes.append(stem_word[:-1] + suffix)

    return words_with_affixes
def add_amharic_adj_affixes(stem_word):
    words_with_affixes = []

    for prefix in amharic_adj_prefixes:
        words_with_affixes.append(prefix + stem_word)

    for suffix in amharic_adj_suffixes:
        words_with_affixes.append(stem_word[:-1] + suffix)

    return words_with_affixes

def find_closest_word(root_words, misspelled_word):
    closest_word = difflib.get_close_matches(misspelled_word, root_words, n=1)
    if closest_word:
        return closest_word[0]
    else:
        return None
def family(char1, char2):
    char1 = Erbata_TIGBERA(char1, RIBI)
    char2 = Erbata_TIGBERA(char2, RIBI)
    if len(char1) <  2 and len(char2)< 2:
      return 1
    elif char1[0] == char2[0]:
        return 1
    return 0

def order(char1, char2):

        char1 = Erbata_TIGBERA(char1, RIBI)
        char2 = Erbata_TIGBERA(char2, RIBI)
        if len(char1) >= 2 and len(char2) >= 2:
          if char1[1] == char2[1]:
            return 1
        if len(char1) < 2 and len(char2) >= 2:
          if char1[0] == char2[1]:
            return 1
        if len(char1) >=  2 and len(char2)< 2:
          if char1[1] == char2[0]:
            return 1
        return 0

def match_words(word1, word2):
    matched_chars = ""
    unmatched_chars1_before = ""
    unmatched_chars1_after = ""
    unmatched_chars2_before = ""
    unmatched_chars2_after = ""

    if word1 is None or word2 is None:
        return matched_chars, unmatched_chars1_before, unmatched_chars1_after, unmatched_chars2_before, unmatched_chars2_after

    # Convert the words into lists of characters
    word1_list = list(word1)
    word2_list = list(word2)

    # Iterate over each character in word1
    for char1 in word1_list:
        # Iterate over each character in word2
        for char2 in word2_list:
            if char1 == char2:
                matched_chars += char1

    if matched_chars:
        # Find the index of the first matched character in word1
        first_match_index = word1.index(matched_chars[0])

        # Extract the characters before and after the matched characters for word1
        unmatched_chars1_before = word1[:first_match_index]
        unmatched_chars1_after = word1[first_match_index + len(matched_chars):]

        # Find the index of the first matched character in word2
        first_match_index = word2.index(matched_chars[0])

        # Extract the characters before and after the matched characters for word2
        unmatched_chars2_before = word2[:first_match_index]
        unmatched_chars2_after = word2[first_match_index + len(matched_chars):]
    else:
        unmatched_chars1_after = word1
        unmatched_chars2_after = word2

    return (
        matched_chars,
        unmatched_chars1_before,
        unmatched_chars1_after,
        unmatched_chars2_before,
        unmatched_chars2_after
    )
    
def compare_words(word1, word2):
    matched, unmatched1_before, unmatched1_after, unmatched_chars2_before, unmatched_chars2_after = match_words(word1, word2)
    # Step 3: Computing average distance between unmatched blocks
    total_distance = 0.0
    comparisons = 0
    unmatched_dif2=0
    unmatched_dif1=0
    XX=0
    if unmatched1_after or unmatched_chars2_after:
        min_length2 = min(len(unmatched1_after), len(unmatched_chars2_after))
        max_length2 = max(len(unmatched1_after), len(unmatched_chars2_after))
        unmatched_dif2 = max_length2 - min_length2
        for i in range(min_length2):
          for j in range(min_length2):
                char1 = unmatched1_after[i]
                char2 = unmatched_chars2_after[j]

                comparisons += 1
                if char1 =='' :
                  total_distance += 0.1
                  
                elif char2 =='':
                  total_distance += 0.1
                  
                elif family(char1, char2) == 1 and order(char1, char2) == 1:
                  total_distance += 1
                  
                elif family(char1, char2) == 1 and order(char1, char2) != 1:
                  total_distance += 0.7
                  
                elif family(char1, char2) != 1 and order(char1, char2) == 1:
                  total_distance += 0.5
                  
                elif family(char1, char2) != 1 and order(char1, char2) != 1:
                    total_distance += 0.3
                    
    if unmatched1_before or unmatched_chars2_before:
        min_length1 = min(len(unmatched1_before), len(unmatched_chars2_before))
        max_length1 = max(len(unmatched1_before), len(unmatched_chars2_before))
        unmatched_dif1 = max_length1 - min_length1
        for i in range(min_length1):

          for j in range(min_length1):
                char1 = unmatched1_before[i]
                char2 = unmatched_chars2_before[j]
                comparisons += 1
                if char1 =='' :
                  total_distance += 0.1
                elif char2 =='':
                  total_distance += 0.1
    
                elif family(char1, char2) == 1 and order(char1, char2) == 1:
                  total_distance += 1
                elif family(char1, char2) == 1 and order(char1, char2) != 1:
                  total_distance += 0.7
                elif family(char1, char2) != 1 and order(char1, char2) == 1:
                  total_distance += 0.5
                elif family(char1, char2) != 1 and order(char1, char2) != 1:
                    total_distance += 0.3
    total_distance += len(matched)
    XX=(unmatched_dif1 + unmatched_dif2)
    yy=(XX/10)
    total_distance =yy+total_distance
    total_distance = float("{:.1f}".format(total_distance))
    comparisons += unmatched_dif1 + unmatched_dif2+len(matched)
    average_distance = total_distance / int(comparisons)
    average_distance = "\033[91m" + str(average_distance) + "\033[0m"  # Set the value of word1 to red color
    return matched, unmatched1_before, unmatched_chars2_before,unmatched1_after, unmatched_chars2_after, total_distance, comparisons, average_distance


# Check if a word is in the noun list
def is_noun(word):
    return word in noun_list

# Check if a word is in the verb list
def is_verb(word):
    return word in verb_list

# Check if a word is in the adjective list
def is_adjective(word):
    return word in adj_list

def remove_amharic_noun_affix(word):
    for prefix in amharic_noun_prefixes:
        if word.startswith(prefix):
            word = word[len(prefix):]
            break
    for suffix in amharic_noun_suffixes:
        if word.endswith(suffix):
            word = word[:-len(suffix)]
            break
    return word#.rstrip(word[-1])

def remove_amharic_verb_affix(word):
    for prefix in amharic_verb_prefixes:
        if word.startswith(prefix):
            word = word[len(prefix):]
            break
    for suffix in amharic_verb_suffixes:
        if word.endswith(suffix):
            word = word[:-len(suffix)]
            break
    return word#.rstrip(word[-1])
def remove_amharic_Adj_affix(word):
    for prefix in amharic_adj_prefixes:
        if word.startswith(prefix):
            word = word[len(prefix):]
            break
    for suffix in amharic_adj_suffixes:
        if word.endswith(suffix):
            word = word[:-len(suffix)]
            break
    return word#.rstrip(word[-1])

def remove_hyphen(word):
    return word.replace("-", "")

# Download the Amharic tokenizer resources from NLTK
nltk.download('punkt')
def remove_last_character(line):
    return line[:-1]


def is_amharic_word(word):
    amharic_alphabet = am  # Add all Amharic characters to the list
    for char in word:
        if char not in amharic_alphabet:
            return False
    return True

def tokenize_amharic_paragraph(paragraph):
    words = paragraph.split()
    return words

def remove_punctuation(word):
    amharic_punctuation = "።'\"፣፤፥.፦፧፨[]=-_{}"
    translator = str.maketrans("", "", string.punctuation + amharic_punctuation)
    word_without_punct = word.translate(translator)
    return word_without_punct



@app.route('/spellcheck', methods=['POST'])
def spell_check():
    data = request.get_json()
    word = data.get('word', '')
    
    newam = Erbata_TIGBERA(word , RIBI)             
    newam3 = remove_amharic_verb_affix(newam)
    print(is_word_in_dictionary(newam3))
    if  is_word_in_dictionary(newam3):
        # Word is in the dictionary
        response = {
            'word': newam3,
            'message': 'The word is present in the dictionary.',
        }
    else:
        # Word is not in the dictionary, find the closest word
        closest_word = find_closest_word(root_list, newam3)
        response = {
            'word': newam3,
            'message': 'The word is not found in the dictionary.',
            'closest_word': closest_word,
        }

    return jsonify(response)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_string=''
        distances_dict = {} 
        close_Aray=[]
        amharic_paragraph = request.form['amharic_paragraph']
        amharic_words = tokenize_amharic_paragraph(amharic_paragraph)
        amharic_words_without_punct = [remove_punctuation(word) for word in amharic_words]
        amharic_words_without_punct = [word for word in amharic_words_without_punct if word]  # Remove empty words
        print(amharic_words_without_punct)
        invalid_words = []
        output_messages = []
        # Capture the printed output
        stdout = sys.stdout
        sys.stdout = StringIO()
        for word in amharic_words_without_punct:
            if not is_amharic_word(word):
                invalid_words.append(word)
        
        if invalid_words:
            error_message = 'Invalid Amharic words: ' + ', '.join(invalid_words)
            return render_template('index.html', error_message=error_message)
        else:
            results = []
            output_messages = []
            for w in amharic_words_without_punct:
                newam = Erbata_TIGBERA(w, RIBI)             
                newam1 = remove_amharic_noun_affix(newam) 
                newam2 = remove_amharic_verb_affix(newam) 
                newam3 = remove_amharic_Adj_affix(newam)
                amharic_word = w# Replace with the string you want to search for
                search_string1 = newam1 
                search_string2 = newam2 
                search_string3 = newam3
                if is_word_in_dictionary(search_string1): 
                    catagory='noun'
                    search_string = search_string1 
                    steam_form = so_called_steam_noun_word(newam1) 
                    message = f"The string '{remove_hyphen(amharic_word)}'{catagory}'' is present in the file."
                    output_messages.append(message)
                elif is_word_in_dictionary(search_string2):
                    catagory=''
                    search_string = search_string2
                    steam_form = so_called_steam_verb_word(newam2)
                    message = f"The string '{remove_hyphen(amharic_word)}'{catagory}'' is present in the file."
                    output_messages.append(message)
        
                elif is_word_in_dictionary(search_string3):
                   search_string = search_string3
                   steam_form = so_called_steam_adj_word(newam3)
                   message = f"The string '{remove_hyphen(amharic_word)}'{catagory}'' is present in the file."
                   output_messages.append(message) 
                else:
                  message =f"The string '{remove_hyphen(amharic_word)}' is not found in the file."
                  output_messages.append(message)
                  closest1 = find_closest_word(root_list, newam)
                  closest = reverse_Erbata(closest1, RIBI) 
                  if is_noun(closest1): 
                     close_Aray = add_amharic_noun_affixes(closest1)
                  elif is_verb(closest1): 
                    close_Aray = add_amharic_verb_affixes(closest1)
                  elif is_adjective(closest1): 
                      close_Aray = add_amharic_adj_affixes(closest1)
                  close_Aray_re = []
                  close_Aray_re_removed_phe = []
                  avaragedist = []
                  for word in close_Aray:
                    manipulated_word = reverse_Erbata(word, RIBI)
                    removed_phe = remove_hyphen(manipulated_word)
                    close_Aray_re.append(manipulated_word)
                    close_Aray_re_removed_phe.append(removed_phe)

                  if closest: 
                    message =f"The spelling of '{w}' {Fore.RED}is incorrect. Did you mean: {Fore.GREEN}{close_Aray_re_removed_phe}{Style.RESET_ALL}"
                    word1 = w

                    for word in close_Aray_re_removed_phe: 
                        matched, unmatched1_before, unmatched_chars2_before, unmatched1_after, unmatched_chars2_after, total_distance, comparisons, average_distance = compare_words(word1, word)
                        avaragedist.append(average_distance)
                        distances_dict[word] = average_distance 
                    sorted_distances = sorted(avaragedist, key=lambda dist: float(re.sub("\x1b\[.*?m", "", dist)))
                    print("Average Distances Distances Dictionary:", distances_dict)
                    highest_value = max(distances_dict, key=distances_dict.get)
                    highest_value_value = distances_dict[highest_value]
                    print("Nearest  Distances Dictionary:", highest_value, "which distance is", highest_value_value)
                  else: 
                      print(f"No close match found for '{search_string}'.")
                  
                output = sys.stdout.getvalue()  # Get the printed output
                output_messages.append({
                   'entered word': amharic_word,
                   'vc form ': newam,
                   'correct':message
               })
            
            return render_template('index.html', valid_paragraph=results, output_messages=output_messages)

    # Handle the GET request
    return render_template('index.html', output_messages=[])  # Pass an empty list for output_messages on GET request

if __name__ == '__main__':
    create_database()
    app.run(debug=False)