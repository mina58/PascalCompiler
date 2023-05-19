import unittest
from Parser.rd_parser import RDParser
from nltk.tree import *
from Scanner.scanner import Scanner
import traceback
class ParserTest(unittest.TestCase):
    def test_basic_program(self):
        source_code = "program test; begin x := 3*2 end."
        scanner = Scanner()
        tokens = scanner.scan(source_code)
        parser = RDParser(tokens)
        try:
            result = parser.parse()
            expected = Tree('Program', [
                Tree('ProgramHeading', ['test']),
                Tree('Block', [
                    Tree('Statement', [
                        Tree('Assignment Statement', [
                            Tree('Variable', ['x']),
                            Tree('Expression', [
                                Tree('Factor', ['3']),
                                '*',
                                Tree('Factor', ['2'])
                            ])
                        ])
                    ])
                ])
            ])
            print("--------------------------------")
            print(expected)
            print("--------------------------------")
            print(result)
            self.assertEqual(result, expected)
        except Exception as e:
            print(f"Exception occurred during parsing: {e}")

    # def test_program_with_statements(self):
    #     source_code = "program test; begin a := b + c; x := y - z; end."
    #     scanner = Scanner()
    #     tokens = scanner.scan(source_code)
    #     parser = RDParser(tokens)
    #     expected = Tree('Program', [
    #         Tree('ProgramHeading', ['test']),
    #         Tree('Block', [
    #             Tree('Statement', [
    #                 Tree('AssignmentStatement', [
    #                     Tree('Variable', ['a']),
    #                     Tree('Expression', [
    #                         Tree('Variable', ['b']),
    #                         '+',
    #                         Tree('Variable', ['c'])
    #                     ])
    #                 ])
    #             ]),
    #             Tree('Statement', [
    #                 Tree('AssignmentStatement', [
    #                     Tree('Variable', ['x']),
    #                     Tree('Expression', [
    #                         Tree('Variable', ['y']),
    #                         '-',
    #                         Tree('Variable', ['z'])
    #                     ])
    #                 ])
    #             ])
    #         ])
    #     ])
    #     result = parser.parse()
    #     print("--------------------------------")
    #     print(expected)
    #     print("--------------------------------")
    #     print(result)
    #     self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
