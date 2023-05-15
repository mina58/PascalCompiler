from .token_types import TokenType
from .operators import operators
from .reserved_words import reserved_words
from .token import Token

import re


class Scanner:
    def __init__(self) -> None:
        self.__identifier_regex = "^[a-z_\$][a-z\d_\$]*$"
        self.__integer_regex = "^[+-]?\d+$"
        self.__real_regex = "^[+-]?\d+.\d+(e[+-]\d+)?$"
        # in some cases there are no space between the operators and the identifiers so we will use this regex to scan
        # for the operators
        self.__operators_regex = "\~|\*|\/|\+|\-|\=|\<\>|\>|\>\=|\<|\<=|\&|\||\!|\:\=|\{|\}|\(|\)|\[|\]|\,|\;|\:|\"|\'"
        self.__comments_regex = '\{.*\}|\{\*(.|\n)*\*\}'
        self.__string_regex = "\'.*\'"

    
    def __identify_lexeme_type(self, lexeme: str) -> TokenType:
        """Returns the token type of the passed lexeme."""
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
    

    def __find_strings(self, source_code: str) -> list:
        """Returns a list of string token objects."""
        strings = re.findall(self.__string_regex, source_code)

        string_tokens = []

        for string in strings:
            token = Token(string, TokenType.StringConstant)
            string_tokens.append(token)

        return string_tokens



    def scan(self, source_code: str) -> list:
        """Returns a token objects stream of the given source code."""
        # remove all the comments from the source_code
        source_code = re.sub(self.__comments_regex, " ", source_code)

        # pascal is case-insensitive, so we first lower all the code and then split the text
        source_code = source_code.lower()

        # split the source code on the operators and the spaces but only keep the operators
        lexemes = [lex.strip() for lex in re.split(f"(\s|{self.__operators_regex})", source_code) if lex.strip()]
        tokens_stream = []
        
        # get all the strings in the source code
        string_tokens = self.__find_strings(source_code)
        
        string_counter = 0
        string_flag = False

        for lexeme in lexemes:
            if string_flag:
                if lexeme == "'":
                    string_flag = False
                    tokens_stream.append(string_tokens[string_counter])
                    string_counter += 1
                continue
            
            if lexeme == "'":
                string_flag = True
                continue
            
            token_type = self.__identify_lexeme_type(lexeme)
            token = Token(lexeme, token_type)
            tokens_stream.append(token)
        
        return tokens_stream
