import unittest

from Parser.Grammar.grammar import Grammar
class TestGrammar(unittest.TestCase):

    def test_valid_grammar_file(self):
        grammar = Grammar('valid_grammar.txt')

        assert grammar.start == 'Program', "Invalid start symbol"

        expected_non_terminals = {
            'Program', 'Heading', 'Declaration', 'Uses', 'Identifiers_List',
            'Identifiers_List_Prime', 'Constant_Declarations', 'Constant_Definitions',
            'Constant_Definitions_Prime', 'Data_Type_Values', 'Type_Declarations',
            'Type_Definitions', 'Type_Definitions_Prime', 'Data_Type', 'Variable_Declarations',
            'Variables_Definition', 'Variables_Definition_Prime', 'Functions_Declarations',
            'One_Function_Declaration', 'Parameters', 'Parameters_Prime', 'Execution', 'Block',
            'Statement_List', 'Statement_List_Prime', 'Statement', 'Assignment_Statement',
            'IF_Statement', 'IF_Statement_Prime', 'IF_Statement_Double_Prime', 'Statement_or_Block',
            'For_Loop', 'Repeat', 'Boolean_Expression', 'Relational_Operator', 'Procedure_Call',
            'Argument_List', 'Parameters_Definition', 'Parameters_List', 'Parameters_List_Prime',
            'Block', 'Expression', 'Expression_Prime', 'Term', 'Term_Prime', 'Factor', 'Factor_Prime',
            'Expression_List', 'Expression_List_Prime', 'Procedures_Declarations',
            'One_Procedure_Declaration'
        }

        assert grammar.non_terminals == expected_non_terminals, "Invalid non-terminals"

        expected_terminals = {
            'identifier', ';', 'uses', ',', '~', 'const', '=', 'integer_constant', 'real_constant',
            'character_constant', 'string_constant', 'true', 'false', 'type', 'var', ':', 'function',
            '(', 'integer', 'string', 'char', 'boolean', 'real', 'begin', 'end', 'if', 'then', 'else',
            'for', 'to', 'do', 'repeat', 'until', 'read', 'readln', 'write', 'writeln', '.',
            '>=', '+', '<>', '/','procedure', '-', ':=', '<=', '*', '>', '<', ')', 'program'
        }

        assert grammar.terminals == expected_terminals, "Invalid terminals"

        expected_grammar = {
            'Program': {
                ('Heading', 'Declaration', 'Execution')
            },
            'Heading': {
                ('program', 'identifier', ';')
            },
            'Declaration': {
                ('Uses', 'Constant_Declarations', 'Type_Declarations', 'Variable_Declarations',
                 'Functions_Declarations', 'Procedures_Declarations')
            },
            'Uses': {
                ('uses', 'Identifiers_List', ';'),
                ('~',)
            },
            'Identifiers_List': {
                ('identifier', 'Identifiers_List_Prime')
            },
            'Identifiers_List_Prime': {
                (',', 'Identifiers_List'),
                ('~',)
            },
            'Constant_Declarations': {
                ('const', 'Constant_Definitions'),
                ('~',)
            },
            'Constant_Definitions': {
                ('identifier', '=', 'Data_Type_Values', ';', 'Constant_Definitions_Prime')
            },
            'Constant_Definitions_Prime': {
                ('Constant_Definitions',),
                ('~',)
            },
            'Data_Type_Values': {
                ('integer_constant',),
                ('real_constant',),
                ('character_constant',),
                ('string_constant',),
                ('true',),
                ('false',)
            },
            'Type_Declarations': {
                ('type', 'Type_Definitions'),
                ('~',)
            },
            'Type_Definitions': {
                ('identifier', '=', 'Data_Type', ';', 'Type_Definitions_Prime')
            },
            'Type_Definitions_Prime': {
                ('Type_Definitions',),
                ('~',)
            },
            'Data_Type': {
                ('integer',),
                ('real',),
                ('char',),
                ('string',),
                ('boolean',),
                ('identifier',)
            },
            'Variable_Declarations': {
                ('var', 'Variables_Definition'),
                ('~',)
            },
            'Variables_Definition': {
                ('Identifiers_List', ':', 'Data_Type', ';', 'Variables_Definition_Prime')
            },
            'Variables_Definition_Prime': {
                ('Variables_Definition',),
                ('~',)
            },
            'Functions_Declarations': {
                ('One_Function_Declaration', ';', 'Functions_Declarations'),
                ('~',)
            },
            'One_Function_Declaration': {
                ('function', 'identifier', 'Parameters', ':', 'Data_Type', ';', 'Block')
            },
            'Parameters': {
                ('(', 'Parameters_Prime',)
            },
            'Parameters_Prime': {
                ('Parameters_List', ')'),
                (')',)
            },
            'Parameters_List': {
                ('Parameters_Definition', 'Parameters_List_Prime',)
            },
            'Parameters_List_Prime': {
                (';', 'Parameters_List'),
                ('~',)
            },
            'Parameters_Definition': {
                ('identifier', ':', 'Data_Type',)
            },
            'Block': {
                ('begin', 'Variable_Declarations', 'Statement_List', 'end',)
            },
            'Statement_List': {
                ('Statement', 'Statement_List_Prime',)
            },
            'Statement_List_Prime': {
                ('Statement_List',),
                ('~',)
            },
            'Statement': {
                ('Assignment_Statement',),
                ('IF_Statement',),
                ('For_Loop',),
                ('Repeat',),
                ('Procedure_Call',)
            },
            'Assignment_Statement': {
                ('identifier', ':=', 'Expression', ';',)
            },
            'IF_Statement': {
                ('if', 'Boolean_Expression', 'then', 'IF_Statement_Prime',)
            },
            'IF_Statement_Prime': {
                ('Statement_or_Block', 'IF_Statement_Double_Prime',)
            },
            'IF_Statement_Double_Prime': {
                ('else', 'Statement_or_Block',),
                ('~',)
            },
            'Statement_or_Block': {
                ('Statement',),
                ('Block',)
            },
            'For_Loop': {
                ('for', 'identifier', ':=', 'Expression', 'to', 'Expression', 'do', 'Statement_or_Block',)
            },
            'Repeat': {
                ('repeat', 'Statement_List', 'until', 'Boolean_Expression', ';',)
            },
            'Boolean_Expression': {
                ('Expression', 'Relational_Operator', 'Expression',)
            },
            'Relational_Operator': {
                ('=',),
                ('<>',),
                ('<',),
                ('>',),
                ('<=',),
                ('>=',)
            },
            'Procedure_Call': {
                ('identifier', '(', 'Argument_List', ')', ';',),
                ('read', '(', 'Argument_List', ')', ';',),
                ('readln', '(', 'Argument_List', ')', ';',),
                ('write', '(', 'Argument_List', ')', ';',),
                ('writeln', '(', 'Argument_List', ')', ';',)
            },
            'Argument_List': {
                ('Expression_List',),
                ('~',)
            },
            'Expression': {
                ('Term', 'Expression_Prime',)
            },
            'Expression_Prime': {
                ('+', 'Term', 'Expression_Prime',),
                ('-', 'Term', 'Expression_Prime',),
                ('~',)
            },
            'Term': {
                ('Factor', 'Term_Prime',)
            },
            'Term_Prime': {
                ('*', 'Factor', 'Term_Prime',),
                ('/', 'Factor', 'Term_Prime',),
                ('~',)
            },
            'Factor': {
                ('identifier', 'Factor_Prime',),
                ('(', 'Expression', ')',),
                ('Data_Type_Values',)
            },
            'Factor_Prime': {
                ('(', 'Argument_List', ')',),
                ('~',)
            },
            'Expression_List': {
                ('Expression', 'Expression_List_Prime',)
            },
            'Expression_List_Prime': {
                (',', 'Expression', 'Expression_List_Prime',),
                ('~',)
            },
            'Procedures_Declarations': {
                ('One_Procedure_Declaration', ';', 'Procedures_Declarations',),
                ('~',)
            },
            'One_Procedure_Declaration': {
                ('procedure', 'identifier', 'Parameters', ';', 'Block',)
            },
            'Execution': {
                ('Block', '.')
            }
        }

        assert grammar.grammar == expected_grammar, "Invalid grammar rules"

    def test_missing_non_terminal_symbol(self):
        # Test if the Grammar class raises an assertion error for a missing non-terminal symbol
        with self.assertRaises(AssertionError):
            grammar = Grammar('missing_non_terminal.txt')

    def test_invalid_non_terminal_symbol(self):
        # Test if the Grammar class raises an assertion error for an invalid non-terminal symbol
        with self.assertRaises(AssertionError):
            grammar = Grammar('invalid_non_terminal.txt')

    def test_null_symbol_error(self):
        # Test if the Grammar class raises an assertion error for invalid use of the null symbol
        with self.assertRaises(AssertionError):
            grammar = Grammar('null_symbol_error.txt')

    def test_retrieve_productions(self):
        # Test if the Grammar class correctly retrieves the productions for a non-terminal symbol
        grammar = Grammar('valid_grammar.txt')
        productions = grammar.get_productions('Program')
        expected_productions = {
            ('Heading', 'Declaration', 'Execution'),
        }
        self.assertEqual(productions, expected_productions)

if __name__ == '__main__':
    unittest.main()
