import nltk
from nltk.draw import TreeWidget
from nltk.draw.util import CanvasFrame
from Scanner.scanner import Scanner
from Parser.SLR.slr_parser import SLRParser
import unittest


def draw_nltk_tree(tree):
    cf = CanvasFrame()
    tc = TreeWidget(cf.canvas(), tree)
    cf.add_widget(tc, 10, 10)
    cf.print_to_file('tree.ps')
    cf.destroy()
    nltk.draw.tree.draw_trees(tree)


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
            print(parser.parsing_table)
            draw_nltk_tree(parse_tree)
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")
        # Print the parse tree

    def test_parsing_table(self):
        # Create a grammar
        grammar_file = "path/to/grammar_file.txt"
        parser = SLRParser(grammar_file)

        # Build the parsing table
        parsing_table = parser.build_parsing_table()

        # Print the parsing table
        parser.print_parsing_table()


