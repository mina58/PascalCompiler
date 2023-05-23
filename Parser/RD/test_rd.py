import unittest

import nltk
import pandas
from nltk.draw import TreeWidget
from nltk.draw.util import CanvasFrame

from Parser.RD.rd_parser import RDParser
from Scanner.scanner import Scanner

import traceback
import tkinter as tk
import pandastable as pt


def draw_nltk_tree(tree):
    cf = CanvasFrame()
    tc = TreeWidget(cf.canvas(), tree)
    cf.add_widget(tc, 10, 10)
    cf.print_to_file('tree.ps')
    cf.destroy()
    nltk.draw.tree.draw_trees(tree)

def display_error_list(error_list):
    df1 = pandas.DataFrame(error_list)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()

class ParserTest(unittest.TestCase):
    def test_one_statement(self):
        source_code = "program test; begin x := 1+3*2; end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            display_error_list(parser.errors)
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_two_statements(self):
        source_code = "program test; begin a := b + c; x := y - z; end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")


    def test_if_statement(self):
        source_code = "program test; begin if a = b then x := y + z; end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_if_else_statement(self):
        source_code = "program test; begin if a = b then x := y + z; else x := y - z; end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_repeat_statement(self):
        source_code = "program test; begin repeat x := y + z; until x = 0; end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_variable_declaration(self):
        source_code = "program test; var x: integer; begin x := 10; end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_procedure_declaration(self):
        source_code = "program test; procedure PrintHello(); begin writeln('Hello, World!'); end; begin PrintHello(); end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            #print(f"Exception occurred during parsing: {e}")
            #get traceback info
            traceback.print_exc()

    def test_function_declaration(self):
        source_code = "program test; function CalculateSum(a: integer , b: integer): integer; begin result := a + b; end; begin writeln(CalculateSum(2, 3)); end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_empty_block(self):
        source_code = "program test; begin end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_assignment_statement(self):
        source_code = "program test; begin x := 10; end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_for_statement(self):
        source_code = "program test; begin for i := 1 to 10 do writeln(i); end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_while_statement(self):
        source_code = "program test; begin while x > 0 do begin x := x - 1; end; end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_nested_statements(self):
        source_code = '''
        program test;
        var x, y, z: integer;
        begin
            x := 1;
            if x = 1 then
            begin
                y := 2;
                if y = 2 then
                begin
                    z := x + y;
                    writeln(z);
                end;
            end;
        end.
        '''
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_and_keyword(self):
        source_code = '''
        program test;
        begin
            if a = 1 and b = 2 then
            begin
                x := 1;
            end;
        end.
        '''
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_or_keyword(self):
        source_code = '''
        program test;
        begin
            if a = 1 or b = 2 then
            begin
                x := 1;
            end;
        end.
        '''
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

##############################################################################################################
    #Invalid test cases
    def test_missing_semicolon(self):
        source_code = "program test begin x := 10; end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_missing_period(self):
        source_code = "program test; begin x := 10; end"
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_missing_begin(self):
        source_code = "program test; x := 10; end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_missing_end(self):
        source_code = "program test; begin x := 10; ."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_missing_program(self):
        source_code = "test; begin x := 10; end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_missing_identifier(self):
        source_code = "program; begin x := 10; end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    def test_misspelled_program(self):
        source_code = "programm test; begin x := 10; end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            draw_nltk_tree(result)
            result.pretty_print()
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")






if __name__ == '__main__':
    unittest.main()
