# Copyright 2018 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
__author__ = 'seanfitz'
import re

from .lemmatizer import lemmatize 

regex_letter_number = r"[a-zA-Z0-9]"
regex_not_letter_number = r"[^a-zA-Z0-9]"
regex_separator = r"[\\?!()\";/\\|`]"

regex_clitics = r"'|:|-|'CH|'ch|'I|'i|'M|'m|'N|'n|'R|'r|'TH|'th|'U|'u|'W|'w"


abbreviations_list = [ "e.e.", "a.y.b.",
            "Mr.", "Jr.", "Ms.", "Mme.", "Mrs.", "Dr.",
            "Ph.D."]


class WelshTokenizer(object):
    def __init__(self):
        pass

    def tokenize(self, string):
        """Used to parce a string into tokens

        This function is to take in a string and return a list of tokens

        Args:
            string(str): This is a string of words or a sentance to be parsed into tokens

        Returns:
            list: a list of tokens from the string passed in.

        Notes:
            Doesn't seem to parse contractions correctly for example don't
            would parse as two tokens 'do' and "n't" and this seems to be not
            what we would want.  Maybe should be "don't" or maybe contractions
            should be expanded into "do not" or "do","not".  This could be
            done with a contraction dictionary and some preprocessing.
        """
        #print ("tokenize: " + string)
        s = string
        s = re.sub('\t', " ", s)
        s = re.sub("(" + regex_separator + ")", " \g<1> ", s)
        s = re.sub("([^0-9]),", "\g<1> , ", s)
        s = re.sub(",([^0-9])", " , \g<1>", s)
        s = re.sub("^(')", "\g<1> ", s)
        s = re.sub("(" + regex_not_letter_number + ")'", "\g<1> '", s)
        s = re.sub("(" + regex_clitics + ")$", " \g<1>", s)
        s = re.sub("(" + regex_clitics + ")(" + regex_not_letter_number + ")", " \g<1> \g<2>", s)

        words = s.strip().split()
        p1 = re.compile(".*" + regex_letter_number + "\\.")
        p2 = re.compile("^([A-Za-z]\\.([A-Za-z]\\.)+|[A-Z][bcdfghj-nptvxz]+\\.)$")

        token_list = []

        for word in words:
            word = lemmatize(word)

            m1 = p1.match(word)
            m2 = p2.match(word)

            if m1 and word not in abbreviations_list and not m2:
                token_list.append(word[0: word.find('.')])
                token_list.append(word[word.find('.')])
            else:
                token_list.append(word)

        return token_list


def tokenize_string(text):
    """To assist with testing strings returns the token list from text

    Args:
        text(str): String to be parsed into tokens

    Returns:
        list: A list of tokens found in the text.
    """
    tk = WelshTokenizer()
    return tk.tokenize(text)

if __name__ == "__main__":
    print(tokenize_string("Beth yw'r tywydd ym Mangor?"))
