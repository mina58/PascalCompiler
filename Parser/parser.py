from Scanner import token_types , reserved_words , token , operators
from Scanner.token import Token
from Scanner.token_types import TokenType
from nltk.tree import *
from Scanner.scanner import Scanner


text = input("Enter Code:")
Tokens = Scanner.scan(text)
errors = []


def Parse():
    pointer=0
    Children=[]
    program_output = Program(pointer)
    Children.append(program_output["node"])

    Node=Tree('Program',Children)


def Program(pointer):
    output = dict()
    children = []

    heading_output = Heading(pointer)
    children.append(heading_output['node'])

    declaration_output = Declaration(heading_output['index'])
    children.append(declaration_output['node'])

    execution_output = Execution(declaration_output['index'])
    children.append(execution_output['node'])

    Node = Tree('Program', children)
    output["node"] = Node
    output["index"] = execution_output["index"]

    return output

def Heading(pointer):
    output = dict()
    children = []

    program_output = Match(TokenType.ProgramKeyword , pointer)
    children.append(program_output['node'])

    identifier_output = Match(TokenType.Identifier , program_output['index'])
    children.append(identifier_output['node'])

    Node = Tree('Heading', children)
    output["node"] = Node
    output["index"] = identifier_output["index"]

    return output

def Declaration(pointer):
    output = dict()
    children = []

    uses_output = Uses(pointer)
    children.append(uses_output['node'])

    constant_declarations_output = ConstantDeclarations(uses_output['index'])
    children.append(constant_declarations_output['node'])

    type_declarations_output = TypeDeclarations(constant_declarations_output['index'])
    children.append(type_declarations_output['node'])

    variable_declaration_output = VariablesDeclaration(type_declarations_output['index'])
    children.append(variable_declaration_output['node'])

    function_declaration_output = FunctionsDeclaration(variable_declaration_output['index'])
    children.append(function_declaration_output['node'])

    procedure_declaration_output = ProcedureDeclaration(function_declaration_output['index'])
    children.append(procedure_declaration_output['node'])

    Node = Tree('Declaration', children)
    output["node"] = Node
    output["index"] = procedure_declaration_output["index"]

    return output


def Uses(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()
    if current['type'] == TokenType.UsesKeyword:
        uses_output = Match(TokenType.UsesKeyword, pointer)
        children.append(uses_output['node'])

        identifiers_list_output = IdentifiersList(uses_output['index'])
        children.append(identifiers_list_output['node'])

        semicolon_output = Match(TokenType.SemiColon, identifiers_list_output['index'])
        children.append(semicolon_output['node'])
    else:
        semicolon_output = None

    Node = Tree('Uses', children)
    output["node"] = Node
    output["index"] = semicolon_output["index"] if semicolon_output else pointer

    return output


def IdentifiersList(pointer):
    output = dict()
    children = []

    identifier_output = Match(TokenType.Identifier , pointer)
    children.append(identifier_output['node'])

    #handling left factoring
    identifiers_list_prime_output = IdentifiersListPrime(identifier_output['index'])
    children.append(identifiers_list_prime_output['node'])

    Node = Tree('Identifiers List', children)
    output["node"] = Node
    output["index"] = identifiers_list_prime_output["index"]

    return output

def IdentifiersListPrime(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.Comma:
        comma_output = Match(TokenType.Comma , pointer)
        children.append(comma_output['node'])

        identifiers_list_output = IdentifiersList(comma_output['index'])
        children.append(identifiers_list_output['node'])
    else:
        identifiers_list_output = None

    Node = Tree('Identifiers List Prime', children)
    output["node"] = Node
    output["index"] = identifiers_list_output["index"] if identifiers_list_output else pointer

    return output


def ConstantDeclarations(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.ConstKeyword:
        const_output = Match(TokenType.ConstKeyword , pointer)
        children.append(const_output['node'])

        constant_definitions_output = ConstantDefinitions(const_output['index'])
        children.append(constant_definitions_output['node'])
    else:
        constant_definitions_output = None

    Node = Tree('Constant Declarations', children)
    output["node"] = Node
    output["index"] = constant_definitions_output["index"] if constant_definitions_output else pointer

    return output


def ConstantDefinitions(pointer):
    output = dict()
    children = []

    identifier_output = Match(TokenType.Identifier , pointer)
    children.append(identifier_output['node'])

    equality_output = Match(TokenType.EqualToOp , identifier_output['index'])
    children.append(equality_output['node'])

    data_type_values_output = DataTypeValues(equality_output['index'])
    children.append(data_type_values_output['index'])

    semicolon_output = Match(TokenType.SemiColon , data_type_values_output['index'])
    children.append(semicolon_output['node'])

    constant_definitions_prime_output = ConstantDefinitionsPrime(semicolon_output['index'])
    children.append(constant_definitions_prime_output['node'])

    Node = Tree('Constant Definitions', children)
    output["node"] = Node
    output["index"] = constant_definitions_prime_output["index"]

    return output

def ConstantDefinitionsPrime(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.Identifier:
        constant_definitions_output = ConstantDefinitions(pointer)
        children.append(constant_definitions_output['node'])
    else:
        constant_definitions_output = None

    Node = Tree('Constant Definitions Prime', children)
    output["node"] = Node
    output["index"] = constant_definitions_output["index"] if constant_definitions_output else pointer

    return output

def DataTypeValues(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.IntegerConstant:
        data_output = Match(TokenType.IntegerConstant , pointer)

    elif current['type'] == TokenType.RealConstant:
        data_output = Match(TokenType.RealConstant , pointer)

    elif current['type'] == TokenType.StringConstant:
        data_output = Match(TokenType.StringConstant, pointer)

    elif current['type'] == TokenType.TrueKeyword:
        data_output = Match(TokenType.TrueKeyword , pointer)

    else:
        data_output = Match(TokenType.FalseKeyword , pointer)

    children.append(data_output['node'])

    Node = Tree('Data Type Values', children)
    output["node"] = Node
    output["index"] = data_output["index"]

    return output

def TypeDeclarations(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.TypeKeyword:
        type_keyword_output = Match(TokenType.TypeKeyword , pointer)
        children.append(type_keyword_output['node'])

        type_definitions_output = TypeDefinitions(type_keyword_output['index'])
        children.append(type_definitions_output['node'])

    else:
        type_definitions_output = None

    Node = Tree('Type Declarations', children)
    output["node"] = Node
    output["index"] = type_definitions_output["index"] if type_definitions_output else pointer

    return output


def TypeDefinitions(pointer):
    output = dict()
    children = []

    identifier_output = Match(TokenType.Identifier , pointer)
    children.append(identifier_output['node'])

    equal_output = Match(TokenType.EqualToOp , identifier_output['index'])
    children.append(equal_output['node'])

    data_type_output = DataType(equal_output['index'])
    children.append(data_type_output['node'])

    semicolon_output = Match(TokenType.SemiColon , data_type_output['index'])
    children.append(semicolon_output['node'])

    type_definitions_prime_output = TypeDefinitionsPrime(semicolon_output['index'])
    children.append(type_definitions_prime_output['node'])

    Node = Tree('Type Definitions', children)
    output["node"] = Node
    output["index"] = type_definitions_prime_output["index"]

    return output


def TypeDefinitionsPrime(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.Identifier:
        type_definitions_output = TypeDefinitions(pointer)
        children.append(type_definitions_output['node'])
    else:
        type_definitions_output = None

    Node = Tree('Type Definitions Prime', children)
    output["node"] = Node
    output["index"] = type_definitions_output["index"] if type_definitions_output else pointer

    return output


def DataType(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.IntegerKeyword:
        data_output = Match(TokenType.IntegerKeyword , pointer)

    elif current['type'] == TokenType.RealKeyword:
        data_output = Match(TokenType.RealKeyword , pointer)

    elif current['type'] == TokenType.CharKeyword:
        data_output = Match(TokenType.CharKeyword , pointer)

    elif current['type'] == TokenType.StringKeyword:
        data_output = Match(TokenType.StringKeyword , pointer)

    elif current['type'] == TokenType.BooleanKeyword:
        data_output = Match(TokenType.BooleanKeyword , pointer)

    else:
        data_output = Match(TokenType.Identifier , pointer)

    children.append(data_output['node'])

    Node = Tree('Data Type', children)
    output["node"] = Node
    output["index"] = data_output["index"]

    return output


def VariablesDeclaration(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.VarKeyword:
        variable_output = Match(TokenType.VarKeyword , pointer)
        children.append(variable_output['node'])

        variables_definition_output = VariablesDefinition(variable_output['index'])
        children.append(variables_definition_output['node'])

    else:
        variables_definition_output = None

    Node = Tree('Variable Declaration', children)
    output["node"] = Node
    output["index"] = variables_definition_output["index"] if variables_definition_output else pointer

    return output

def VariablesDefinition(pointer):
    output = dict()
    children = []

    identifiers_list_output = IdentifiersList(pointer)
    children.append(identifiers_list_output['node'])

    variable_definition_prime_output = VariablesDefinitionPrime(identifiers_list_output['index'])
    children.append(variable_definition_prime_output['node'])

    Node = Tree('Variable Definition', children)
    output["node"] = Node
    output["index"] = variable_definition_prime_output["index"]

    return output

def VariablesDefinitionPrime(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.Colon:
        colon_output = Match(TokenType.Colon , pointer)
        children.append(colon_output)

        data_type_output = DataType(colon_output['index'])
        children.append(data_type_output['node'])

        semicolon_output = Match(TokenType.SemiColon , data_type_output['index'])
        children.append(semicolon_output['node'])

        variable_definition_prime_output = VariablesDefinition(semicolon_output['index'])
        children.append(variable_definition_prime_output['node'])

    else:
        equal_output = Match(TokenType.EqualToOp , pointer)
        children.append(equal_output['node'])

        variable_definition_prime_output = DataType(equal_output['index'])
        children.append(variable_definition_prime_output['node'])

    Node = Tree('Variables Definition Prime', children)
    output["node"] = Node
    output["index"] = variable_definition_prime_output["index"]

    return output

def FunctionsDeclaration(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.FunctionKeyword:
        one_function_declaration_output = OneFunctionDeclaration(pointer)
        children.append(one_function_declaration_output['node'])

        semicolon_output = Match(TokenType.SemiColon , one_function_declaration_output['index'])
        children.append(semicolon_output['node'])

        functions_declaration_output = FunctionsDeclaration(semicolon_output['index'])
        children.append(functions_declaration_output['node'])

    else:
        functions_declaration_output = None

    Node = Tree('Functions Declarations', children)
    output["node"] = Node
    output["index"] = functions_declaration_output["index"] if functions_declaration_output else pointer

    return output

def OneFunctionDeclaration(pointer):
    output = dict()
    children = []

    function_keyword_output = Match(TokenType.FunctionKeyword , pointer)
    children.append(function_keyword_output['node'])

    identifier_output = Match(TokenType.Identifier , function_keyword_output['index'])
    children.append(identifier_output['node'])

    parameters_output = Parameters(identifier_output['index'])
    children.append(parameters_output['node'])

    colon_output = Match(TokenType.Colon , parameters_output['index'])
    children.append(colon_output['node'])

    data_type_output = DataType(colon_output['index'])
    children.append(data_type_output['node'])

    semicolon_output = Match(TokenType.SemiColon , data_type_output['index'])
    children.append(semicolon_output['node'])

    block_output = Block(semicolon_output['index'])
    children.append(block_output['node'])

    Node = Tree('Function Declaration', children)
    output["node"] = Node
    output["index"] = block_output["index"]

    return output

def Parameters(pointer):
    output = dict()
    children = []

    open_parenthesis_output = Match(TokenType.OpenParenthesis , pointer)
    children.append(open_parenthesis_output['node'])

    parameters_prime_output = ParametersPrime(open_parenthesis_output['index'])
    children.append(parameters_prime_output['node'])

    Node = Tree('Parameters', children)
    output["node"] = Node
    output["index"] = parameters_prime_output["index"]

    return output

def ParametersPrime(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.CloseParenthesis:
        close_parenthesis_output = Match(TokenType.CloseParenthesis , pointer)
        children.append(close_parenthesis_output['node'])

    else:
        parameter_list_output = ParametersList(pointer)
        children.append(parameter_list_output)

        close_parenthesis_output = Match(TokenType.CloseParenthesis, parameter_list_output['index'])
        children.append(close_parenthesis_output['node'])

    Node = Tree('Parameters Prime', children)
    output["node"] = Node
    output["index"] = close_parenthesis_output["index"]

    return output

def ParametersList(pointer):
    output = dict()
    children = []

    parameter_definition_output = ParameterDefinition(pointer)
    children.append(parameter_definition_output['node'])

    parameters_list_prime_output = ParametersListPrime(parameter_definition_output['index'])
    children.append(parameters_list_prime_output['node'])

    Node = Tree('Parameters List', children)
    output["node"] = Node
    output["index"] = parameters_list_prime_output["index"]

    return output

def ParametersListPrime(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.Comma:
        comma_output = Match(TokenType.Comma , pointer)
        children.append(comma_output['node'])

        parameters_list_output = ParametersList(comma_output['index'])
        children.append(parameters_list_output['node'])

    else:
        parameters_list_output = None

    Node = Tree('Parameters List Prime', children)
    output["node"] = Node
    output["index"] = parameters_list_output["index"] if parameters_list_output else pointer

    return output

def ParameterDefinition(pointer):
    output = dict()
    children = []

    identifier_output = Match(TokenType.Identifier , pointer)
    children.append(identifier_output['node'])

    colon_output = Match(TokenType.Colon , identifier_output['index'])
    children.append(colon_output['node'])

    data_type_output = DataType(colon_output['index'])
    children.append(data_type_output['node'])

    Node = Tree('Parameter Definition', children)
    output["node"] = Node
    output["index"] = data_type_output["index"]

    return output

def Block(pointer):
    output = dict()
    children = []

    begin_keyword_output = Match(TokenType.BeginKeyword , pointer)
    children.append(begin_keyword_output['node'])

    variables_declaration_output = VariablesDeclaration(begin_keyword_output['index'])
    children.append(variables_declaration_output['node'])

    statement_list_output = StatementList(variables_declaration_output['index'])
    children.append(statement_list_output['node'])

    end_keyword_output = Match(TokenType.EndKeyword , statement_list_output['index'])
    children.append(end_keyword_output['node'])

    Node = Tree('Block', children)
    output["node"] = Node
    output["index"] = end_keyword_output["index"]

    return output

def StatementList(pointer):
    pass

def ProcedureDeclaration(pointer):
    pass

def Execution(pointer):
    pass


########################################################################################
def Match(a, pointer):
    output = dict()
    if pointer < len(Tokens):
        temp = Tokens[pointer].to_dict()
        if temp['token_type'] == a:
            pointer += 1
            output["node"] = [temp['Lex']]
            output["index"] = pointer
            return output
        else:
            output["node"] = ["error"]
            output["index"] = pointer + 1
            errors.append("Syntax error : " + temp['Lex'] + " Expected dot")
            return output
    else:
        output["node"] = ["error"]
        output["index"] = pointer + 1
        return output
########################################################################################