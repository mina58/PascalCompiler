from token_types import TokenType
from operators import operators
from reserved_words import reserved_words
from token import Token

import re


class Scanner:
    def __init__(self) -> None:
        self.__identifier_regex = "^[a-z_\$][a-z\d_\$]*$"
        self.__integer_regex = "^[+-]?\d+$"
        self.__real_regex = "^[+-]?\d+.\d+(e[+-]\d+)?$"
        # in some cases there are no space between the operators and the identifiers so we will use this regex to scan
        # for the operators
        self.__operators_regex = "(\~|\*|\/|\+|\-|\=|\<\>|\>|\>\=|\<|\<=|\&|\||\!|\:\=|\{|\}|\(|\)|\[|\]|\,|\;|\:|\"|\')"

    
    def __identify_lexeme_type(self, lexeme: str) -> TokenType:
        token_type = TokenType.Error
        if lexeme in reserved_words:
            token_type = reserved_words[lexeme]
        elif lexeme in operators:
            token_type = operators[lexeme]
        elif re.match(self.__integer_regex, lexeme):
            token_type = TokenType.IntegerConstant
        elif re.match(self.__real_regex, lexeme):
            token_type = TokenType.RealConstant
        elif re.match(self.__identifier_regex, lexeme):
            token_type = TokenType.Identifier

        return token_type


    def scan(self, source_code: str) -> list:
        # pascal is case insensitive so we first lower all the code and then split the text
        lexemes = source_code.lower().split()
        tokens_stream = []


        for lexeme in lexemes:
            # some times re.split() produces empty strings
            split_lexeme = [lex for lex in re.split(f"{self.__operators_regex}", lexeme) if lex] 

            # check if there are any operators that are sticking to other keywords
            if len(split_lexeme) > 1:
                for lex in split_lexeme:
                    token_type = self.__identify_lexeme_type(lex)
                    token = Token(lex, token_type)
                    tokens_stream.append(token)
            else:
                token_type = self.__identify_lexeme_type(lexeme)
                token = Token(lexeme, token_type)
                tokens_stream.append(token)

        return tokens_stream
    