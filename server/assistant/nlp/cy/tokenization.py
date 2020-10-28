#!/usr/bin/env python3
#coding: utf-8
import re
import datetime
from  dateutil import parser

valid_letters_lower = 'aáàâäbcdeéèêëfghiíìîïjlmnoóòôöprstuúùûüwẃẁŵẅyýỳŷÿ'
valid_letters_upper = valid_letters_lower.upper()

regex_letter_number = r"[" + valid_letters_lower + valid_letters_upper + r"0-9]"
regex_not_letter_number = r"[^" + valid_letters_lower + valid_letters_upper + r"0-9]"
regex_separator = r"[\\?!()\";/\\|`]"

regex_clitics = r"'|:|-|'CH|'ch|'I|'i|'M|'m|'N|'n|'R|'r|'TH|'th|'U|'u|'W|'w"


class Tokenization(object):

    def __init__(self):
        pass

        
    def detokenize(self, string):
        s = string
        s = ' '.join(s)
        s = re.sub(r' (' + regex_clitics + ')', r"\g<1>", s)
        s = re.sub(r' (' + regex_separator + ')', r"\g<1>", s)
        return s.strip()


    def tokenize(self, string):
        s = string
        s = re.sub('\t', " ", s)
        s = re.sub("(" + regex_separator + ")", " \g<1> ", s)
        s = re.sub("(" + regex_not_letter_number + ")'", "\g<1> '", s)
        s = re.sub("(" + regex_clitics + ")$", " \g<1>", s)
        s = re.sub("(" + regex_clitics + ")(" + regex_not_letter_number + ")", " \g<1> \g<2>", s)

        return s.strip().split()


    def tokens_to_words(self, tokens):
        for t in tokens: 
           self.determine_token(t)

        return tokens

    def determine_token(self, token):
       if self.is_token_float(token):
           print (token, 'float')
       elif self.is_token_datetime(token):
           print (token, 'datetime')

 
    def is_token_float(self, token):
        return token.replace('.','').lstrip('-').isdigit() 

 
    def is_token_datetime(self, token):
        return any(char.isdigit() for char in token)


    def round_float_token(self, orig_float):
        return int(round(float(orig_float)))


    def token_to_datetime(self, time_string):
        return parser.parse(time_string)


    def datetime_token_to_hours_words(self, orig_datetime):
        hour = 0
        ampm = ''

        dt = parser.parse(orig_datetime)
        hour = dt.hour
        if hour == 12:
            return "hanner dydd"

        if hour == 0 or hour == 24:
            return "hanner nos"

        template = "%s o'r gloch %s"

        if hour > 12 and hour < 18:
            hour = hour - 12
            ampm = "yn y prynhawn"
        elif hour >= 18:
            hour = hour - 12
            ampm = "yn y nos"
        else:
            ampm = "yn y bore"
            
        return template % (hour, ampm)   
            


if __name__ == "__main__":

    t = Tokenizer()
    toks = t.tokenize("Beth yw'r tywydd ym Mangor?")    
    print(toks)
    print(t.detokenize(toks))

