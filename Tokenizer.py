from tokenize import tokenize
from io import BytesIO
import pandas as pd
import sys
import math

def read_file(file):
    file_string = ""
    with open(file, 'r', encoding='utf-8') as f:
        file_string = f.read()
    return file_string

def tokenize_string(s):
    result = []
    g = tokenize(BytesIO(s.encode('utf-8')).readline)
    for _, tokval, _, _, _ in g:
        result.append(tokval)
    return result

def find_subsequence(token_list):
    untokened_source = "".join(token_list)
    token_dict = {}
    start = 0
    end = 1
    while end < len(token_list):
        subsequence = token_list[start:end]
        calculate_tokens(subsequence, token_dict, untokened_source)
        end += 1
    correct_tokens = eliminate_single_tokens(token_dict)
    return correct_tokens

def calculate_tokens(subsequence, token_dict, untokened_source):
    start = len(subsequence) - 1
    while start >= 0:
        current_token = subsequence[start:]
        current_token_string = ''.join(current_token)
        if current_token_string not in token_dict:
            count = untokened_source.count(current_token_string)
            length = len(current_token)
            token_dict[current_token_string] = [count, length]
        start -= 1

def eliminate_single_tokens(token_dict):
    correct_tokens = {}
    for token, token_details in token_dict.items():
        if token_details[1] > 1:
            correct_tokens[token] = token_details
    return correct_tokens
    
def read_files(file_list):
    results = []
    for file in file_list:
        file_string = read_file(file)
        result = tokenize_string(file_string)
        results.append(result)
    return results
    
def find_common_subsequence(tokenized_list):
    token_dict = {}
    tokens = tokenized_list[0]
    token_dict = find_subsequence(tokens)
    i = 1
    while i < len(tokenized_list):
        other_token_dict = find_subsequence(tokenized_list[i])
        uncommon_keys = []
        for key in token_dict.keys():
            if key in other_token_dict:
                old_count = token_dict[key][0]
                new_count = old_count + other_token_dict[key][0]
                token_dict[key] = [new_count, other_token_dict[key][1]]
            else:
                uncommon_keys.append(key)
        for key in uncommon_keys:
            del token_dict[key]
        i += 1
    return token_dict

def to_csv(token_dict):
	csv_dict = {"score": [], "tokens": [], "count": [], "sourcecode": []}
	for token_value, token_details in token_dict.items():
		csv_dict["tokens"].append(token_details[1])
		csv_dict["count"].append(token_details[0])
		score = math.log(token_details[0], 2) * math.log(token_details[1], 2)
		csv_dict["score"].append(score)
		csv_dict["sourcecode"].append(token_value)
	df = pd.DataFrame(csv_dict)
	df.sort_values(by='score', ascending=False, inplace=True)
	df.to_csv('data.csv', index=None)

def say_hello():
    print("Hello World")
    
if "__main__" == __name__:
    file_list = sys.argv[1:]
    tokenized_list = read_files(file_list)
    common_subsequence = find_common_subsequence(tokenized_list)
    to_csv(common_subsequence)