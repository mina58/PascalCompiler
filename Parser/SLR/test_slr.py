import nltk
from nltk.draw import TreeWidget
from nltk.draw.util import CanvasFrame
from Scanner.scanner import Scanner
from Parser.SLR.slr_parser import SLRParser
import unittest
import traceback

def draw_nltk_tree(tree):
    tree.draw()


class SLRParserTest(unittest.TestCase):
    def test_parser(self):
        # Create a grammar
        grammar_file = "../Grammar/grammar.txt"
        parser = SLRParser(grammar_file)

        # Create tokens for testing
        scanner = Scanner()
        tokens = scanner.scan("program test; begin x := 1+3*2; end.")

        # Parse the tokens
        try:
            parse_tree = parser.parse(tokens)
            print(parse_tree)
            draw_nltk_tree(parse_tree)
        except Exception as e:
            traceback.print_exc()
            # print(f"Exception occurred during parsing: {e}")

    def test_parsing_table(self):
        # Create a grammar
        grammar_file = "path/to/grammar_file.txt"
        parser = SLRParser(grammar_file)

        # Build the parsing table
        parsing_table = parser.build_parsing_table()

        # Print the parsing table
        parser.print_parsing_table()


