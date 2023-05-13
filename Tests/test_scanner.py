import unittest

from Scanner.scanner import Scanner
from Scanner.token_types import TokenType
from Scanner.token import Token


class ScannerTest(unittest.TestCase):
    def test_basic_expression(self):
        source_code = "b := a + c"
        scanner = Scanner()
        result = scanner.scan(source_code)
        token_1 = Token('b', TokenType.Identifier)
        token_2 = Token(':=', TokenType.AssignmentOp)
        token_3 = Token('a', TokenType.Identifier)
        token_4 = Token('+', TokenType.AddOp)
        token_5 = Token('c', TokenType.Identifier)
        expected = [token_1, token_2, token_3, token_4, token_5]
        for _ in range(len(expected)):
            self.assertEqual(result[_], expected[_], f"token: {result[_]}, expected: {expected[_]}")
            
    
    def test_expression_with_no_space(self):
        source_code = "b:=a+c"
        scanner = Scanner()
        result = scanner.scan(source_code)
        token_1 = Token('b', TokenType.Identifier)
        token_2 = Token(':=', TokenType.AssignmentOp)
        token_3 = Token('a', TokenType.Identifier)
        token_4 = Token('+', TokenType.AddOp)
        token_5 = Token('c', TokenType.Identifier)
        expected = [token_1, token_2, token_3, token_4, token_5]
        for _ in range(len(expected)):
            self.assertEqual(result[_], expected[_], f"token: {result[_]}, expected: {expected[_]}")
            
            
    def test_single_line_comments(self):
        source_code ="""
        {this is a comment}
        """
        scanner = Scanner()
        result = scanner.scan(source_code)
        self.assertEqual(len(result), 0)
        
        
    def test_multi_line_comments(self):
        source_code ="""
        {*this is a comment
        still a comment*}
        """
        scanner = Scanner()
        result = scanner.scan(source_code)
        self.assertEqual(len(result), 0)
        
        
    def test_invalid_multi_line_comments(self):
        source_code ="""
        {this is a comment
        still a comment}
        """
        scanner = Scanner()
        result = scanner.scan(source_code)
        self.assertNotEqual(len(result), 0)
        
        
    def test_strings_1(self):
        source_code = """
        'this is a string'
        """
        scanner = Scanner()
        result = scanner.scan(source_code)
        expected = Token("'this is a string'", TokenType.String)
        self.assertEqual(result[0], expected, result[0])
        
    
    def test_strings_2(self):
        source_code = """
        string s := 'this is a string'
        """
        scanner = Scanner()
        token_1 = Token('string', TokenType.StringKeyword)
        token_2 = Token('s', TokenType.Identifier)
        token_3 = Token(':=', TokenType.AssignmentOp)
        token_4 = Token("'this is a string'", TokenType.String)
        result = scanner.scan(source_code)
        expected = [token_1, token_2, token_3, token_4]
        for _ in range(len(expected)):
            self.assertEqual(result[_], expected[_], f"token: {result[_]}, expected: {expected[_]}")

if __name__ == '__main__':
    unittest.main()
