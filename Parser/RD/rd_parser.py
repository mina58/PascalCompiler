from Scanner.token_types import TokenType
from nltk.tree import *


class RDParser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.errors = []
    def parse(self):
        pointer=0
        Children=[]
        program_output = self.program(pointer)
        Children.append(program_output["node"])

        node=Tree('Program',Children)


        return self.remove_empty_nodes(node)


    def program(self, pointer):
        output = dict()
        children = []

        heading_output = self.heading(pointer)
        children.append(heading_output['node'])

        declaration_output = self.declaration(heading_output['index'])
        children.append(declaration_output['node'])

        execution_output = self.execution(declaration_output['index'])
        children.append(execution_output['node'])

        Node = Tree('Program', children)
        output["node"] = Node
        output["index"] = execution_output["index"]

        return output

    def heading(self, pointer):
        output = dict()
        children = []

        program_output = self.match(TokenType.ProgramKeyword, pointer)
        children.append(program_output['node'])

        identifier_output = self.match(TokenType.Identifier , program_output['index'])
        children.append(identifier_output['node'])

        semicolon_output = self.match(TokenType.SemiColon , identifier_output['index'])
        children.append(semicolon_output['node'])

        Node = Tree('Heading', children)
        output["node"] = Node
        output["index"] = semicolon_output["index"]

        return output

    def declaration(self, pointer):
        output = dict()
        children = []

        uses_output = self.uses(pointer)
        children.append(uses_output['node'])

        constant_declarations_output = self.constant_declarations(uses_output['index'])
        children.append(constant_declarations_output['node'])

        type_declarations_output = self.type_declarations(constant_declarations_output['index'])
        children.append(type_declarations_output['node'])

        variable_declaration_output = self.variables_declaration(type_declarations_output['index'])
        children.append(variable_declaration_output['node'])

        function_declaration_output = self.functions_declaration(variable_declaration_output['index'])
        children.append(function_declaration_output['node'])

        procedure_declaration_output = self.procedures_declaration(function_declaration_output['index'])
        children.append(procedure_declaration_output['node'])

        Node = Tree('Declaration', children)
        output["node"] = Node
        output["index"] = procedure_declaration_output["index"]

        return output


    def uses(self, pointer):
        output = dict()
        children = []
        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.UsesKeyword:
            uses_output = self.match(TokenType.UsesKeyword, pointer)
            children.append(uses_output['node'])

            identifiers_list_output = self.identifiers_list(uses_output['index'])
            children.append(identifiers_list_output['node'])

            semicolon_output = self.match(TokenType.SemiColon, identifiers_list_output['index'])
            children.append(semicolon_output['node'])
        else:
            semicolon_output = None

        Node = Tree('Uses', children)
        output["node"] = Node
        output["index"] = semicolon_output["index"] if semicolon_output else pointer

        return output


    def identifiers_list(self, pointer):
        output = dict()
        children = []

        identifier_output = self.match(TokenType.Identifier , pointer)
        children.append(identifier_output['node'])

        #handling left factoring
        identifiers_list_prime_output = self.identifiers_list_prime(identifier_output['index'])
        children.append(identifiers_list_prime_output['node'])

        Node = Tree('Identifiers List', children)
        output["node"] = Node
        output["index"] = identifiers_list_prime_output["index"]

        return output

    def identifiers_list_prime(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.Comma:
            comma_output = self.match(TokenType.Comma , pointer)
            children.append(comma_output['node'])

            identifiers_list_output = self.identifiers_list(comma_output['index'])
            children.append(identifiers_list_output['node'])
        else:
            identifiers_list_output = None

        Node = Tree('Identifiers List Prime', children)
        output["node"] = Node
        output["index"] = identifiers_list_output["index"] if identifiers_list_output else pointer

        return output


    def constant_declarations(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.ConstKeyword:
            const_output = self.match(TokenType.ConstKeyword , pointer)
            children.append(const_output['node'])

            constant_definitions_output = self.constant_definitions(const_output['index'])
            children.append(constant_definitions_output['node'])
        else:
            constant_definitions_output = None

        Node = Tree('Constant Declarations', children)
        output["node"] = Node
        output["index"] = constant_definitions_output["index"] if constant_definitions_output else pointer

        return output


    def constant_definitions(self, pointer):
        output = dict()
        children = []

        identifier_output = self.match(TokenType.Identifier , pointer)
        children.append(identifier_output['node'])

        equality_output = self.match(TokenType.EqualToOp , identifier_output['index'])
        children.append(equality_output['node'])

        data_type_values_output = self.data_type_values(equality_output['index'])
        children.append(data_type_values_output['index'])

        semicolon_output = self.match(TokenType.SemiColon , data_type_values_output['index'])
        children.append(semicolon_output['node'])

        constant_definitions_prime_output = self.constant_definitions_prime(semicolon_output['index'])
        children.append(constant_definitions_prime_output['node'])

        Node = Tree('Constant Definitions', children)
        output["node"] = Node
        output["index"] = constant_definitions_prime_output["index"]

        return output

    def constant_definitions_prime(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.Identifier:
            constant_definitions_output = self.constant_definitions(pointer)
            children.append(constant_definitions_output['node'])
        else:
            constant_definitions_output = None

        Node = Tree('Constant Definitions Prime', children)
        output["node"] = Node
        output["index"] = constant_definitions_output["index"] if constant_definitions_output else pointer

        return output

    def data_type_values(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.IntegerConstant:
            data_output = self.match(TokenType.IntegerConstant , pointer)

        elif current['type'] == TokenType.RealConstant:
            data_output = self.match(TokenType.RealConstant , pointer)

        elif current['type'] == TokenType.StringConstant:
            data_output = self.match(TokenType.StringConstant, pointer)

        elif current['type'] == TokenType.TrueKeyword:
            data_output = self.match(TokenType.TrueKeyword , pointer)

        elif current['type'] == TokenType.FalseKeyword:
            data_output = self.match(TokenType.FalseKeyword , pointer)
        else:
            data_output = self.fail_match('Data Type Value', current, pointer)

        children.append(data_output['node'])

        Node = Tree('Data Type Values', children)
        output["node"] = Node
        output["index"] = data_output["index"]

        return output

    def type_declarations(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.TypeKeyword:
            type_keyword_output = self.match(TokenType.TypeKeyword , pointer)
            children.append(type_keyword_output['node'])

            type_definitions_output = self.type_definitions(type_keyword_output['index'])
            children.append(type_definitions_output['node'])

        else:
            type_definitions_output = None

        Node = Tree('Type Declarations', children)
        output["node"] = Node
        output["index"] = type_definitions_output["index"] if type_definitions_output else pointer

        return output


    def type_definitions(self, pointer):
        output = dict()
        children = []

        identifier_output = self.match(TokenType.Identifier , pointer)
        children.append(identifier_output['node'])

        equal_output = self.match(TokenType.EqualToOp , identifier_output['index'])
        children.append(equal_output['node'])

        data_type_output = self.data_type(equal_output['index'])
        children.append(data_type_output['node'])

        semicolon_output = self.match(TokenType.SemiColon , data_type_output['index'])
        children.append(semicolon_output['node'])

        type_definitions_prime_output = self.type_definitions_prime(semicolon_output['index'])
        children.append(type_definitions_prime_output['node'])

        Node = Tree('Type Definitions', children)
        output["node"] = Node
        output["index"] = type_definitions_prime_output["index"]

        return output


    def type_definitions_prime(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.Identifier:
            type_definitions_output = self.type_definitions(pointer)
            children.append(type_definitions_output['node'])
        else:
            type_definitions_output = None

        Node = Tree('Type Definitions Prime', children)
        output["node"] = Node
        output["index"] = type_definitions_output["index"] if type_definitions_output else pointer

        return output


    def data_type(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.IntegerKeyword:
            data_output = self.match(TokenType.IntegerKeyword , pointer)

        elif current['type'] == TokenType.RealKeyword:
            data_output = self.match(TokenType.RealKeyword , pointer)

        elif current['type'] == TokenType.CharKeyword:
            data_output = self.match(TokenType.CharKeyword , pointer)

        elif current['type'] == TokenType.StringKeyword:
            data_output = self.match(TokenType.StringKeyword , pointer)

        elif current['type'] == TokenType.BooleanKeyword:
            data_output = self.match(TokenType.BooleanKeyword , pointer)

        elif current['type'] == TokenType.Identifier:
            data_output = self.match(TokenType.Identifier , pointer)
        else:
            data_output = self.fail_match('Data Type', current, pointer)

        children.append(data_output['node'])

        Node = Tree('Data Type', children)
        output["node"] = Node
        output["index"] = data_output["index"]

        return output


    def variables_declaration(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.VarKeyword:
            variable_output = self.match(TokenType.VarKeyword , pointer)
            children.append(variable_output['node'])

            variables_definition_output = self.variables_definition(variable_output['index'])
            children.append(variables_definition_output['node'])

        else:
            variables_definition_output = None

        Node = Tree('Variable Declaration', children)
        output["node"] = Node
        output["index"] = variables_definition_output["index"] if variables_definition_output else pointer

        return output

    def variables_definition(self, pointer):
        output = dict()
        children = []

        identifiers_list_output = self.identifiers_list(pointer)
        children.append(identifiers_list_output['node'])

        colon_output = self.match(TokenType.Colon , identifiers_list_output['index'])
        children.append(colon_output['node'])

        data_type_output = self.data_type(colon_output['index'])
        children.append(data_type_output['node'])

        semicolon_output = self.match(TokenType.SemiColon , data_type_output['index'])
        children.append(semicolon_output['node'])

        variable_definition_prime_output = self.variables_definition_prime(semicolon_output['index'])
        children.append(variable_definition_prime_output['node'])

        Node = Tree('Variable Definition', children)
        output["node"] = Node
        output["index"] = variable_definition_prime_output["index"]

        return output

    def variables_definition_prime(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.Identifier:
            variable_definition_prime_output = self.variables_definition(pointer)
            children.append(variable_definition_prime_output['node'])

        else:
            variable_definition_prime_output = None

        Node = Tree('Variables Definition Prime', children)
        output["node"] = Node
        output["index"] = variable_definition_prime_output["index"] if variable_definition_prime_output else pointer

        return output

    def functions_declaration(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.FunctionKeyword:
            one_function_declaration_output = self.one_function_declaration(pointer)
            children.append(one_function_declaration_output['node'])

            semicolon_output = self.match(TokenType.SemiColon , one_function_declaration_output['index'])
            children.append(semicolon_output['node'])

            functions_declaration_output = self.functions_declaration(semicolon_output['index'])
            children.append(functions_declaration_output['node'])

        else:
            functions_declaration_output = None

        Node = Tree('Functions Declarations', children)
        output["node"] = Node
        output["index"] = functions_declaration_output["index"] if functions_declaration_output else pointer

        return output

    def one_function_declaration(self, pointer):
        output = dict()
        children = []

        function_keyword_output = self.match(TokenType.FunctionKeyword , pointer)
        children.append(function_keyword_output['node'])

        identifier_output = self.match(TokenType.Identifier , function_keyword_output['index'])
        children.append(identifier_output['node'])

        parameters_output = self.parameters(identifier_output['index'])
        children.append(parameters_output['node'])

        colon_output = self.match(TokenType.Colon , parameters_output['index'])
        children.append(colon_output['node'])

        data_type_output = self.data_type(colon_output['index'])
        children.append(data_type_output['node'])

        semicolon_output = self.match(TokenType.SemiColon , data_type_output['index'])
        children.append(semicolon_output['node'])

        block_output = self.block(semicolon_output['index'])
        children.append(block_output['node'])

        Node = Tree('Function Declaration', children)
        output["node"] = Node
        output["index"] = block_output["index"]

        return output

    def parameters(self, pointer):
        output = dict()
        children = []

        open_parenthesis_output = self.match(TokenType.OpenParenthesis , pointer)
        children.append(open_parenthesis_output['node'])

        parameters_prime_output = self.parameters_prime(open_parenthesis_output['index'])
        children.append(parameters_prime_output['node'])

        Node = Tree('Parameters', children)
        output["node"] = Node
        output["index"] = parameters_prime_output["index"]

        return output

    def parameters_prime(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.CloseParenthesis:
            close_parenthesis_output = self.match(TokenType.CloseParenthesis , pointer)
            children.append(close_parenthesis_output['node'])

        elif current['type'] == TokenType.Identifier:
            parameter_list_output = self.parameters_list(pointer)
            children.append(parameter_list_output['node'])

            close_parenthesis_output = self.match(TokenType.CloseParenthesis, parameter_list_output['index'])
            children.append(close_parenthesis_output['node'])

        else:
            close_parenthesis_output = self.fail_match('Identifier or Close Parenthesis', current, pointer)

        Node = Tree('Parameters Prime', children)
        output["node"] = Node
        output["index"] = close_parenthesis_output["index"]

        return output

    def parameters_list(self, pointer):
        output = dict()
        children = []

        parameter_definition_output = self.parameter_definition(pointer)
        children.append(parameter_definition_output['node'])

        parameters_list_prime_output = self.parameters_list_prime(parameter_definition_output['index'])
        children.append(parameters_list_prime_output['node'])

        Node = Tree('Parameters List', children)
        output["node"] = Node
        output["index"] = parameters_list_prime_output["index"]

        return output

    def parameters_list_prime(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.Comma:
            comma_output = self.match(TokenType.Comma , pointer)
            children.append(comma_output['node'])

            parameters_list_output = self.parameters_list(comma_output['index'])
            children.append(parameters_list_output['node'])

        else:
            parameters_list_output = None

        Node = Tree('Parameters List Prime', children)
        output["node"] = Node
        output["index"] = parameters_list_output["index"] if parameters_list_output else pointer

        return output

    def parameter_definition(self, pointer):
        output = dict()
        children = []

        identifier_output = self.match(TokenType.Identifier , pointer)
        children.append(identifier_output['node'])

        colon_output = self.match(TokenType.Colon , identifier_output['index'])
        children.append(colon_output['node'])

        data_type_output = self.data_type(colon_output['index'])
        children.append(data_type_output['node'])

        Node = Tree('Parameter Definition', children)
        output["node"] = Node
        output["index"] = data_type_output["index"]

        return output

    def block(self, pointer):
        output = dict()
        children = []

        begin_keyword_output = self.match(TokenType.BeginKeyword , pointer)
        children.append(begin_keyword_output['node'])

        variables_declaration_output = self.variables_declaration(begin_keyword_output['index'])
        children.append(variables_declaration_output['node'])

        statement_list_output = self.statement_list(variables_declaration_output['index'])
        children.append(statement_list_output['node'])

        end_keyword_output = self.match(TokenType.EndKeyword , statement_list_output['index'])
        children.append(end_keyword_output['node'])

        Node = Tree('Block', children)
        output["node"] = Node
        output["index"] = end_keyword_output["index"]

        return output

    def statement_list(self, pointer):
        output = dict()
        children = []

        statement_output = self.statement(pointer)
        children.append(statement_output['node'])

        statement_list_prime_output = self.statement_list_prime(statement_output['index'])
        children.append(statement_list_prime_output['node'])

        Node = Tree('Statement List', children)
        output["node"] = Node
        output["index"] = statement_list_prime_output["index"]

        return output

    def statement_list_prime(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] in [TokenType.Identifier , TokenType.IfKeyword , TokenType.ForKeyword , TokenType.RepeatKeyword,
                               TokenType.ReadKeyword , TokenType.ReadlnKeyword , TokenType.WriteKeyword , TokenType.WritelnKeyword]:
            statement_list_prime_output = self.statement_list(pointer)
            children.append(statement_list_prime_output['node'])

        else:
            statement_list_prime_output = None

        Node = Tree('Statement List Prime', children)
        output["node"] = Node
        output["index"] = statement_list_prime_output["index"] if statement_list_prime_output else pointer

        return output

    def statement(self, pointer):
        output = dict()
        children = []
        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output
        current = self.tokens[pointer].as_dict()

        if current['type'] in [TokenType.ReadKeyword , TokenType.ReadlnKeyword , TokenType.WriteKeyword , TokenType.WritelnKeyword]:
            statement_output = self.procedure_call(pointer)
        elif current['type'] == TokenType.Identifier:
            next_token = self.tokens[pointer + 1].as_dict()
            if next_token['type'] == TokenType.OpenParenthesis:
                statement_output = self.procedure_call(pointer)
            elif next_token['type'] == TokenType.AssignmentOp:
                statement_output = self.assignment(pointer)
            else:
                statement_output = self.fail_match('Identifier Follower',self.tokens[pointer].as_dict(),pointer+1)

        elif current['type'] == TokenType.IfKeyword:
            statement_output = self.if_statement(pointer)

        elif current['type'] == TokenType.ForKeyword:
            statement_output = self.for_loop(pointer)

        elif current['type'] == TokenType.RepeatKeyword:
            statement_output = self.repeat(pointer)

        elif current['type'] == TokenType.WhileKeyword:
            statement_output = self.while_loop(pointer)

        else:
            statement_output = self.fail_match('Statement',self.tokens[pointer].as_dict(),pointer)

        children.append(statement_output['node'])

        Node = Tree('Statement', children)
        output["node"] = Node
        output["index"] = statement_output["index"]

        return output


    def assignment(self, pointer):
        output = dict()
        children = []

        identifier_output = self.match(TokenType.Identifier , pointer)
        children.append(identifier_output['node'])

        assignment_operator_output = self.match(TokenType.AssignmentOp , identifier_output['index'])
        children.append(assignment_operator_output['node'])

        expression_output = self.expression(assignment_operator_output['index'])
        children.append(expression_output['node'])

        semicolon_output = self.match(TokenType.SemiColon , expression_output['index'])
        children.append(semicolon_output['node'])

        Node = Tree('Assignment Statement', children)
        output["node"] = Node
        output["index"] = semicolon_output["index"]

        return output

    def if_statement(self, pointer):
        output = dict()
        children = []

        if_output = self.match(TokenType.IfKeyword , pointer)
        children.append(if_output['node'])

        boolean_expression_output = self.boolean_expression(if_output['index'])
        children.append(boolean_expression_output['node'])

        then_output = self.match(TokenType.ThenKeyword , boolean_expression_output['index'])
        children.append(then_output['node'])

        if_prime_output = self.if_statement_prime(then_output['index'])
        children.append(if_prime_output['node'])

        optional_semicolon_output = self.optional_semi_colon(if_prime_output['index'])
        children.append(optional_semicolon_output['node'])

        Node = Tree('IF Statement', children)
        output["node"] = Node
        output["index"] = optional_semicolon_output["index"]

        return output

    def if_statement_prime(self, pointer):
        output = dict()
        children = []

        statement_or_block_output = self.statement_or_block(pointer)
        children.append(statement_or_block_output['node'])

        if_double_prime_output = self.if_statement_double_prime(statement_or_block_output['index'])
        children.append(if_double_prime_output['node'])

        Node = Tree('IF Statement Prime', children)
        output["node"] = Node
        output["index"] = if_double_prime_output["index"]

        return output

    def if_statement_double_prime(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.ElseKeyword:
            else_output = self.match(TokenType.ElseKeyword , pointer)
            children.append(else_output['node'])

            final_output = self.statement_or_block(else_output['index'])
            children.append(final_output['node'])

        else:
            final_output = None

        Node = Tree('IF Statement Double Prime', children)
        output["node"] = Node
        output["index"] = final_output["index"] if final_output else pointer

        return output


    def statement_or_block(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.BeginKeyword:
            current_output = self.block(pointer)

        elif current['type'] in [TokenType.ReadKeyword , TokenType.ReadlnKeyword , TokenType.WriteKeyword , TokenType.WritelnKeyword,
            TokenType.Identifier , TokenType.IfKeyword , TokenType.ForKeyword , TokenType.RepeatKeyword , TokenType.WhileKeyword]:
            current_output = self.statement(pointer)

        else:
            current_output = self.fail_match('Statement or Block',current,pointer)

        children.append(current_output['node'])
        Node = Tree('Statement or Block', children)
        output["node"] = Node
        output["index"] = current_output["index"]

        return output

    def for_loop(self, pointer):
        output = dict()
        children = []

        for_output = self.match(TokenType.ForKeyword , pointer)
        children.append(for_output['node'])

        identifier_output = self.match(TokenType.Identifier , for_output['index'])
        children.append(identifier_output['node'])

        assignment_output = self.match(TokenType.AssignmentOp , identifier_output['index'])
        children.append(assignment_output['node'])

        expression1_output = self.expression(assignment_output['index'])
        children.append(expression1_output['node'])

        to_output = self.match(TokenType.ToKeyword , expression1_output['index'])
        children.append(to_output['node'])

        expression2_output = self.expression(to_output['index'])
        children.append(expression2_output['node'])

        do_output = self.match(TokenType.DoKeyword , expression2_output['index'])
        children.append(do_output['node'])

        statement_or_block_output = self.statement_or_block(do_output['index'])
        children.append(statement_or_block_output['node'])

        optional_semicolon_output = self.optional_semi_colon(statement_or_block_output['index'])
        children.append(optional_semicolon_output['node'])

        Node = Tree('For Loop', children)
        output["node"] = Node
        output["index"] = optional_semicolon_output["index"]

        return output

    def repeat(self, pointer):
        output = dict()
        children = []

        repeat_output = self.match(TokenType.RepeatKeyword , pointer)
        children.append(repeat_output['node'])

        statement_list_output = self.statement_list(repeat_output['index'])
        children.append(statement_list_output['node'])

        until_output = self.match(TokenType.UntilKeyword , statement_list_output['index'])
        children.append(until_output['node'])

        boolean_expression_output = self.boolean_expression(until_output['index'])
        children.append(boolean_expression_output['node'])

        semi_colon_output = self.match(TokenType.SemiColon , boolean_expression_output['index'])
        children.append(semi_colon_output['node'])

        Node = Tree('Repeat', children)
        output["node"] = Node
        output["index"] = semi_colon_output["index"]

        return output

    def while_loop(self, pointer):
        output = dict()
        children = []

        while_output = self.match(TokenType.WhileKeyword , pointer)
        children.append(while_output['node'])

        boolean_expression_output = self.boolean_expression(while_output['index'])
        children.append(boolean_expression_output['node'])

        do_output = self.match(TokenType.DoKeyword , boolean_expression_output['index'])
        children.append(do_output['node'])

        statement_or_block_output = self.statement_or_block(do_output['index'])
        children.append(statement_or_block_output['node'])

        optional_semi_colon_output = self.optional_semi_colon(statement_or_block_output['index'])
        children.append(optional_semi_colon_output['node'])

        Node = Tree('While Loop', children)
        output["node"] = Node
        output["index"] = optional_semi_colon_output["index"]

        return output


    def optional_semi_colon(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.SemiColon:
            semi_colon_output = self.match(TokenType.SemiColon , pointer)
            children.append(semi_colon_output['node'])

        else:
            semi_colon_output = None

        Node = Tree('Optional Semicolon', children)
        output["node"] = Node
        output["index"] = semi_colon_output["index"] if semi_colon_output else pointer

        return output

    def boolean_expression(self, pointer):
        output = dict()
        children = []

        logical_expression_output = self.logical_expression(pointer)
        children.append(logical_expression_output['node'])

        boolean_expression_double_prime_output = self.boolean_expression_double_prime(logical_expression_output['index'])
        children.append(boolean_expression_double_prime_output['node'])

        Node = Tree('Boolean Expression', children)
        output["node"] = Node
        output["index"] = boolean_expression_double_prime_output["index"]

        return output

    def boolean_expression_double_prime(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] in [TokenType.OrKeyword , TokenType.AndKeyword]:
            boolean_expression_prime_output = self.boolean_expression_prime(pointer)
            children.append(boolean_expression_prime_output['node'])
        else:
            boolean_expression_prime_output = None

        Node = Tree('Boolean Expression Double Prime', children)
        output["node"] = Node
        output["index"] = boolean_expression_prime_output['index'] if boolean_expression_prime_output else pointer

        return output

    def boolean_expression_prime(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current_token = self.tokens[pointer].as_dict()

        if current_token['type'] == TokenType.OrKeyword:
            first_output = self.match(TokenType.OrKeyword , pointer)
        elif current_token['type'] == TokenType.AndKeyword:
            first_output = self.match(TokenType.AndKeyword , pointer)
        else:
            first_output = self.fail_match('Logical Connective' , current_token , pointer)

        children.append(first_output['node'])

        boolean_expression_output = self.boolean_expression(first_output['index'])
        children.append(boolean_expression_output['node'])

        Node = Tree('Boolean Expression Prime', children)
        output["node"] = Node
        output["index"] = boolean_expression_output["index"]

        return output

    def logical_expression(self, pointer):
        output = dict()
        children = []

        expression1_output = self.expression(pointer)
        children.append(expression1_output['node'])

        relational_operator_output = self.relational_operator(expression1_output['index'])
        children.append(relational_operator_output['node'])

        expression2_output = self.expression(relational_operator_output['index'])
        children.append(expression2_output['node'])

        Node = Tree('Logical Expression', children)
        output["node"] = Node
        output["index"] = expression2_output["index"]

        return output

    def relational_operator(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.EqualToOp:
            relational_operator_output = self.match(TokenType.EqualToOp , pointer)

        elif current['type'] == TokenType.NotEqualToOp:
            relational_operator_output = self.match(TokenType.NotEqualToOp , pointer)

        elif current['type'] == TokenType.LessThanOp:
            relational_operator_output = self.match(TokenType.LessThanOp , pointer)

        elif current['type'] == TokenType.GreaterThanOp:
            relational_operator_output = self.match(TokenType.GreaterThanOp , pointer)

        elif current['type'] == TokenType.LessThanOrEqualOp:
            relational_operator_output = self.match(TokenType.LessThanOrEqualOp , pointer)

        elif current['type'] == TokenType.GreaterThanOrEqualOp:
            relational_operator_output = self.match(TokenType.GreaterThanOrEqualOp , pointer)
        else:
            relational_operator_output = self.fail_match('Relational Operator' , current , pointer)

        children.append(relational_operator_output['node'])
        Node = Tree('Relational Operator', children)
        output["node"] = Node
        output["index"] = relational_operator_output["index"]

        return output

    def procedure_call(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.Identifier:
            first_output = self.match(TokenType.Identifier , pointer)

        elif current['type'] == TokenType.ReadKeyword:
            first_output = self.match(TokenType.ReadKeyword , pointer)

        elif current['type'] == TokenType.ReadlnKeyword:
            first_output = self.match(TokenType.ReadlnKeyword , pointer)

        elif current['type'] == TokenType.WritelnKeyword:
            first_output = self.match(TokenType.WritelnKeyword , pointer)

        elif current['type'] == TokenType.WriteKeyword:
            first_output = self.match(TokenType.WriteKeyword , pointer)
        else:
            first_output = self.fail_match('Procedure Call' , current , pointer)

        children.append(first_output['node'])

        open_parenthesis_output = self.match(TokenType.OpenParenthesis , first_output['index'])
        children.append(open_parenthesis_output['node'])

        argument_list_output = self.argument_list(open_parenthesis_output['index'])
        children.append(argument_list_output['node'])

        closed_parenthesis_output = self.match(TokenType.CloseParenthesis , argument_list_output['index'])
        children.append(closed_parenthesis_output['node'])

        semi_colon_output = self.match(TokenType.SemiColon , closed_parenthesis_output['index'])
        children.append(semi_colon_output['node'])

        Node = Tree('Procedure Call', children)
        output["node"] = Node
        output["index"] = semi_colon_output["index"]

        return output

    def procedures_declaration(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.ProcedureKeyword:
            one_procedure_declaration_output = self.one_procedure_declaration(pointer)
            children.append(one_procedure_declaration_output['node'])

            semicolon_output = self.match(TokenType.SemiColon , one_procedure_declaration_output['index'])
            children.append(semicolon_output['node'])

            procedures_declaration_output = self.procedures_declaration(semicolon_output['index'])
            children.append(procedures_declaration_output['node'])

        else:
            procedures_declaration_output = None

        Node = Tree('Procedures Declaration', children)
        output["node"] = Node
        output["index"] = procedures_declaration_output["index"] if procedures_declaration_output else pointer

        return output

    def one_procedure_declaration(self, pointer):
        output = dict()
        children = []

        procedure_output = self.match(TokenType.ProcedureKeyword , pointer)
        children.append(procedure_output['node'])

        identifier_output = self.match(TokenType.Identifier , procedure_output['index'])
        children.append(identifier_output['node'])

        parameters_output = self.parameters(identifier_output['index'])
        children.append(parameters_output['node'])

        semicolon_output = self.match(TokenType.SemiColon , parameters_output['index'])
        children.append(semicolon_output['node'])

        block_output = self.block(semicolon_output['index'])
        children.append(block_output['node'])

        Node = Tree('One Procedure Declaration', children)
        output["node"] = Node
        output["index"] = block_output["index"]

        return output
    def execution(self, pointer):
        output = dict()
        children = []

        block_output = self.block(pointer)
        children.append(block_output['node'])

        dot_output = self.match(TokenType.Dot , block_output['index'])
        children.append(dot_output['node'])

        Node = Tree('Execution', children)
        output["node"] = Node
        output["index"] = dot_output["index"]

        return output


    def expression(self, pointer):
        output = dict()
        children = []

        term_output = self.term(pointer)
        children.append(term_output['node'])

        expression_prime_output = self.expression_prime(term_output['index'])
        children.append(expression_prime_output['node'])

        Node = Tree('Expression', children)
        output["node"] = Node
        output["index"] = expression_prime_output["index"]

        return output

    def expression_prime(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.AddOp:
            add_op_output = self.match(TokenType.AddOp , pointer)
            children.append(add_op_output['node'])

            term_output = self.term(add_op_output['index'])
            children.append(term_output['node'])

            expression_prime_output = self.expression_prime(term_output['index'])
            children.append(expression_prime_output['node'])

        elif current['type'] == TokenType.SubtractOp:
            sub_op_output = self.match(TokenType.SubtractOp , pointer)
            children.append(sub_op_output['node'])

            term_output = self.term(sub_op_output['index'])
            children.append(term_output['node'])

            expression_prime_output = self.expression_prime(term_output['index'])
            children.append(expression_prime_output['node'])

        else:
            expression_prime_output = None

        Node = Tree('Expression Prime', children)
        output["node"] = Node
        output["index"] = expression_prime_output["index"] if expression_prime_output else pointer

        return output

    def term(self, pointer):
        output = dict()
        children = []

        factor_output = self.factor(pointer)
        children.append(factor_output['node'])

        term_prime_output = self.term_prime(factor_output['index'])
        children.append(term_prime_output['node'])

        Node = Tree('Term', children)
        output["node"] = Node
        output["index"] = term_prime_output["index"]

        return output

    def term_prime(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.MultiplyOp:
            operator_output = self.match(TokenType.MultiplyOp , pointer)
            children.append(operator_output['node'])

            factor_output = self.factor(operator_output['index'])
            children.append(factor_output['node'])

            term_prime_output = self.term_prime(factor_output['index'])
            children.append(term_prime_output['node'])

        elif current['type'] == TokenType.DivideOp:
            operator_output = self.match(TokenType.DivideOp, pointer)
            children.append(operator_output['node'])

            factor_output = self.factor(operator_output['index'])
            children.append(factor_output['node'])

            term_prime_output = self.term_prime(factor_output['index'])
            children.append(term_prime_output['node'])

        else:
            term_prime_output = None

        Node = Tree('Term Prime', children)
        output["node"] = Node
        output["index"] = term_prime_output["index"] if term_prime_output else pointer

        return output

    def factor(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.Identifier:
            identifier_output = self.match(TokenType.Identifier , pointer)
            children.append(identifier_output['node'])

            final_output = self.factor_prime(identifier_output['index'])
            children.append(final_output['node'])

        elif current['type'] == TokenType.OpenParenthesis:
            open_parenthesis_output = self.match(TokenType.OpenParenthesis , pointer)
            children.append(open_parenthesis_output['node'])

            expression_output = self.expression(open_parenthesis_output['index'])
            children.append(expression_output['node'])

            final_output = self.match(TokenType.CloseParenthesis , expression_output['index'])
            children.append(final_output['node'])

        elif current['type'] in [TokenType.IntegerConstant, TokenType.RealConstant, TokenType.StringConstant, TokenType.TrueKeyword , TokenType.FalseKeyword]:
            #final_output = self.number(pointer)
            final_output = self.data_type_values(pointer)
            children.append(final_output['node'])

        else:
            final_output = self.fail_match('Factor', current,pointer)

        Node = Tree('Factor', children)
        output["node"] = Node
        output["index"] = final_output["index"]

        return output

    def factor_prime(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.OpenParenthesis:
            open_parenthesis_output = self.match(TokenType.OpenParenthesis, pointer)
            children.append(open_parenthesis_output['node'])

            argument_list_output = self.argument_list(open_parenthesis_output['index'])
            children.append(argument_list_output['node'])

            final_output = self.match(TokenType.CloseParenthesis, argument_list_output['index'])
            children.append(final_output['node'])

        else:
            final_output = None

        Node = Tree('Factor Prime', children)
        output["node"] = Node
        output["index"] = final_output["index"] if final_output else pointer

        return output

    def number(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.IntegerConstant:
            final_output = self.match(TokenType.IntegerConstant , pointer)
        else:
            final_output = self.match(TokenType.RealConstant , pointer)

        children.append(final_output['node'])

        Node = Tree('Number', children)
        output["node"] = Node
        output["index"] = final_output["index"]

        return output


    def expression_list(self, pointer):
        output = dict()
        children = []

        expression_output = self.expression(pointer)
        children.append(expression_output['node'])

        expression_list_prime_output = self.expression_list_prime(expression_output['index'])
        children.append(expression_list_prime_output['node'])

        Node = Tree('Expression List', children)
        output["node"] = Node
        output["index"] = expression_list_prime_output["index"]

        return output

    def expression_list_prime(self, pointer):
        output = dict()
        children = []

        if pointer >= len(self.tokens):
            # Handle end of token list
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.Comma:
            comma_output = self.match(TokenType.Comma , pointer)
            children.append(comma_output['node'])

            expression_output = self.expression(comma_output['index'])
            children.append(expression_output['node'])

            expression_list_prime_output = self.expression_list_prime(expression_output['index'])
            children.append(expression_list_prime_output['node'])

        else:
            expression_list_prime_output = None

        Node = Tree('Expression List Prime', children)
        output["node"] = Node
        output["index"] = expression_list_prime_output["index"] if expression_list_prime_output else pointer

        return output

    def argument_list(self, pointer):
        output = dict()
        children = []

        current = self.tokens[pointer].as_dict()

        if current['type'] == TokenType.CloseParenthesis:
            argument_list_output = None
        elif current['type'] in [TokenType.Identifier, TokenType.IntegerConstant, TokenType.RealConstant, TokenType.StringConstant,
                                 TokenType.TrueKeyword , TokenType.FalseKeyword, TokenType.OpenParenthesis]:
            argument_list_output = self.expression_list(pointer)
            children.append(argument_list_output['node'])

        else:
            argument_list_output = self.fail_match('Argument List', current,pointer)


        Node = Tree('Argument List', children)
        output["node"] = Node
        output["index"] = argument_list_output["index"] if argument_list_output else pointer

        return output


    ########################################################################################
    def remove_empty_nodes(self, node):
        if isinstance(node, str):
            return node

        # Recursively process child nodes
        children = [self.remove_empty_nodes(child) for child in node]

        # Remove empty child nodes
        children = [child for child in children if child]

        # If all child nodes were removed, return None
        if not children:
            return None

        # Update the children of the current node
        node.clear()
        node.extend(children)

        return node

    def match(self, expected_token_type, pointer):
        output = dict()
        if pointer < len(self.tokens):
            actual_token_type = self.tokens[pointer].as_dict()
            if actual_token_type['type'] == expected_token_type:
                pointer += 1
                output["node"] = [actual_token_type['lexeme']]
                output["index"] = pointer
                return output
            else:
                return self.fail_match(expected_token_type.name, actual_token_type, pointer)
        else:
            output["node"] = ["error"]
            output["index"] = pointer + 1
            return output
    def fail_match(self, expected, actual, pointer):
        output = dict()
        output["node"] = ["error"]
        output["index"] = pointer
        self.errors.append("Syntax error found : " + actual['lexeme'] + " but Expected " + expected )
        return output

    ########################################################################################