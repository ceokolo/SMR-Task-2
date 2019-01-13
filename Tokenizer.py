from tokenize import tokenize
from io import BytesIO
import sys

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
    correct_tokens = eliminate_single_or_empty_tokens(token_dict)
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

def eliminate_single_or_empty_tokens(token_dict):
    correct_tokens = {}
    for token, token_details in token_dict.items():
        if token_details[0] > 1 and token.strip() != "":
            correct_tokens[token] = token_details
    return correct_tokens

file_string = read_file('hello.py')
print(tokenize_string(file_string))