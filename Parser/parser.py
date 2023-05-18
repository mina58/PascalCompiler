from Scanner.token_types import TokenType, token_types_map
from nltk.tree import *
from Scanner.scanner import Scanner

scanner = Scanner()
text = input("Enter Code:")
Tokens = scanner.scan(text)
errors = []


def Parse():
    pointer=0
    Children=[]
    program_output = Program(pointer)
    Children.append(program_output["node"])

    Node=Tree('Program',Children)

    return Node


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

    procedure_declaration_output = ProceduresDeclaration(function_declaration_output['index'])
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

    colon_output = Match(TokenType.Colon , identifiers_list_output['index'])
    children.append(colon_output['node'])

    data_type_output = DataType(colon_output['index'])
    children.append(data_type_output['node'])

    semicolon_output = Match(TokenType.SemiColon , data_type_output['index'])
    children.append(semicolon_output['node'])

    variable_definition_prime_output = VariablesDefinitionPrime(semicolon_output['index'])
    children.append(variable_definition_prime_output['node'])

    Node = Tree('Variable Definition', children)
    output["node"] = Node
    output["index"] = variable_definition_prime_output["index"]

    return output

def VariablesDefinitionPrime(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.Identifier:
        variable_definition_prime_output = VariablesDefinition(pointer)
        children.append(variable_definition_prime_output['node'])

    else:
        variable_definition_prime_output = None

    Node = Tree('Variables Definition Prime', children)
    output["node"] = Node
    output["index"] = variable_definition_prime_output["index"] if variable_definition_prime_output else pointer

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
    output = dict()
    children = []

    statement_output = Statement(pointer)
    children.append(statement_output['node'])

    statement_list_prime_output = StatementListPrime(statement_output['index'])
    children.append(statement_list_prime_output['node'])

    Node = Tree('Statement List', children)
    output["node"] = Node
    output["index"] = statement_list_prime_output["index"]

    return output

def StatementListPrime(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] in [TokenType.Identifier , TokenType.IfKeyword , TokenType.ForKeyword , TokenType.RepeatKeyword,
                           TokenType.ReadKeyword , TokenType.ReadlnKeyword , TokenType.WriteKeyword , TokenType.WritelnKeyword]:
        statement_list_prime_output = StatementList(pointer)
        children.append(statement_list_prime_output['node'])

    else:
        statement_list_prime_output = None

    Node = Tree('Statement List Prime', children)
    output["node"] = Node
    output["index"] = statement_list_prime_output["index"] if statement_list_prime_output else pointer

    return output

def Statement(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.Identifier:
        statement_output = Assignment(pointer)

    elif current['type'] == TokenType.IfKeyword:
        statement_output = IfStatement(pointer)

    elif current['type'] == TokenType.ForKeyword:
        statement_output = ForLoop(pointer)

    elif current['type'] == TokenType.RepeatKeyword:
        statement_output = Repeat(pointer)

    else: #else it is a procedure call
        statement_output = ProcedureCall(pointer)

    children.append(statement_output['node'])

    Node = Tree('Statement', children)
    output["node"] = Node
    output["index"] = statement_output["index"]

    return output


def Assignment(pointer):
    output = dict()
    children = []

    identifier_output = Match(TokenType.Identifier , pointer)
    children.append(identifier_output['node'])

    assignment_operator_output = Match(TokenType.AssignmentOp , identifier_output['index'])
    children.append(assignment_operator_output['node'])

    expression_output = Expression(assignment_operator_output['index'])
    children.append(expression_output['node'])

    Node = Tree('Assignment Statement', children)
    output["node"] = Node
    output["index"] = expression_output["index"]

    return output

def IfStatement(pointer):
    output = dict()
    children = []

    if_output = Match(TokenType.IfKeyword , pointer)
    children.append(if_output['node'])

    boolean_expression_output = BooleanExpression(if_output['index'])
    children.append(boolean_expression_output['node'])

    then_output = Match(TokenType.ThenKeyword , boolean_expression_output['index'])
    children.append(then_output['node'])

    if_prime_output = IfStatementPrime(then_output['index'])
    children.append(if_prime_output['node'])

    Node = Tree('IF Statement', children)
    output["node"] = Node
    output["index"] = if_prime_output["index"]

    return output

def IfStatementPrime(pointer):
    output = dict()
    children = []

    statement_or_block_output = StatementOrBlock(pointer)
    children.append(statement_or_block_output['node'])

    if_double_prime_output = IfStatementDoublePrime(statement_or_block_output['index'])
    children.append(if_double_prime_output['node'])

    Node = Tree('IF Statement Prime', children)
    output["node"] = Node
    output["index"] = if_double_prime_output["index"]

    return output

def IfStatementDoublePrime(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.ElseKeyword:
        else_output = Match(TokenType.ElseKeyword , pointer)
        children.append(else_output['node'])

        final_output = StatementOrBlock(else_output['index'])
        children.append(final_output['node'])

    else:
        final_output = None

    Node = Tree('IF Statement Double Prime', children)
    output["node"] = Node
    output["index"] = final_output["index"] if final_output else pointer

    return output


def StatementOrBlock(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.BeginKeyword:
        current_output = Block(pointer)

    else:
        current_output = Statement(pointer)

    children.append(current_output['node'])
    Node = Tree('Statement or Block', children)
    output["node"] = Node
    output["index"] = current_output["index"]

    return output

def ForLoop(pointer):
    output = dict()
    children = []

    for_output = Match(TokenType.ForKeyword , pointer)
    children.append(for_output['node'])

    identifier_output = Match(TokenType.Identifier , for_output['index'])
    children.append(identifier_output['node'])

    assignment_output = Match(TokenType.AssignmentOp , identifier_output['index'])
    children.append(assignment_output['node'])

    expression1_output = Expression(assignment_output['index'])
    children.append(expression1_output['node'])

    to_output = Match(TokenType.ToKeyword , expression1_output['index'])
    children.append(to_output['node'])

    expression2_output = Expression(assignment_output['index'])
    children.append(expression2_output['node'])

    do_output = Match(TokenType.DoKeyword , expression2_output['index'])
    children.append(do_output['node'])

    statement_or_block_output = StatementOrBlock(do_output['index'])
    children.append(statement_or_block_output['node'])

    Node = Tree('For Loop', children)
    output["node"] = Node
    output["index"] = statement_or_block_output["index"]

    return output

def Repeat(pointer):
    output = dict()
    children = []

    repeat_output = Match(TokenType.RepeatKeyword , pointer)
    children.append(repeat_output['node'])

    statement_list_output = StatementList(repeat_output['index'])
    children.append(statement_list_output['node'])

    until_output = Match(TokenType.UntilKeyword , statement_list_output['index'])
    children.append(until_output['node'])

    boolean_expression_output = BooleanExpression(until_output['index'])
    children.append(boolean_expression_output['node'])

    Node = Tree('Repeat', children)
    output["node"] = Node
    output["index"] = boolean_expression_output["index"]

    return output

def BooleanExpression(pointer):
    output = dict()
    children = []

    expression1_output = Expression(pointer)
    children.append(expression1_output['node'])

    relational_operator_output = RelationalOperator(expression1_output['index'])
    children.append(relational_operator_output['node'])

    expression2_output = Expression(relational_operator_output['index'])
    children.append(expression2_output['node'])

    Node = Tree('Boolean Expression', children)
    output["node"] = Node
    output["index"] = expression2_output["index"]

    return output

def RelationalOperator(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.EqualToOp:
        relational_operator_output = Match(TokenType.EqualToOp , pointer)

    elif current['type'] == TokenType.NotEqualToOp:
        relational_operator_output = Match(TokenType.NotEqualToOp , pointer)

    elif current['type'] == TokenType.LessThanOp:
        relational_operator_output = Match(TokenType.LessThanOp , pointer)

    elif current['type'] == TokenType.GreaterThanOp:
        relational_operator_output = Match(TokenType.GreaterThanOp , pointer)

    elif current['type'] == TokenType.LessThanOrEqualOp:
        relational_operator_output = Match(TokenType.LessThanOrEqualOp , pointer)

    else:
        relational_operator_output = Match(TokenType.GreaterThanOrEqualOp , pointer)

    children.append(relational_operator_output['node'])
    Node = Tree('Relational Operator', children)
    output["node"] = Node
    output["index"] = relational_operator_output["index"]

    return output

def ProcedureCall(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.Identifier:
        first_output = Match(TokenType.Identifier , pointer)

    elif current['type'] == TokenType.ReadKeyword:
        first_output = Match(TokenType.ReadKeyword , pointer)

    elif current['type'] == TokenType.ReadlnKeyword:
        first_output = Match(TokenType.ReadlnKeyword , pointer)

    elif current['type'] == TokenType.WritelnKeyword:
        first_output = Match(TokenType.WritelnKeyword , pointer)

    else:
        first_output = Match(TokenType.WriteKeyword , pointer)

    open_parenthesis_output = Match(TokenType.OpenParenthesis , first_output['index'])
    children.append(open_parenthesis_output['node'])

    expression_list_output = ExpressionList(open_parenthesis_output['index'])
    children.append(expression_list_output['node'])

    closed_parenthesis_output = Match(TokenType.CloseParenthesis , expression_list_output['index'])
    children.append(closed_parenthesis_output['node'])

    Node = Tree('Procedure Call', children)
    output["node"] = Node
    output["index"] = closed_parenthesis_output["index"]

    return output

def ProceduresDeclaration(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.ProcedureKeyword:
        one_procedure_declaration_output = OneProcedureDeclaration(pointer)
        children.append(one_procedure_declaration_output['node'])

        semicolon_output = Match(TokenType.SemiColon , one_procedure_declaration_output['index'])
        children.append(semicolon_output['node'])

        procedures_declaration_output = ProceduresDeclaration(semicolon_output['index'])
        children.append(procedures_declaration_output['node'])

    else:
        procedures_declaration_output = None

    Node = Tree('Procedures Declaration', children)
    output["node"] = Node
    output["index"] = procedures_declaration_output["index"] if procedures_declaration_output else pointer

    return output

def OneProcedureDeclaration(pointer):
    output = dict()
    children = []

    procedure_output = Match(TokenType.ProcedureKeyword , pointer)
    children.append(procedure_output['node'])

    identifier_output = Match(TokenType.Identifier , procedure_output['index'])
    children.append(identifier_output['node'])

    parameters_output = Parameters(identifier_output['index'])
    children.append(parameters_output['node'])

    semicolon_output = Match(TokenType.SemiColon , parameters_output['index'])
    children.append(semicolon_output['node'])

    block_output = Block(semicolon_output['index'])
    children.append(block_output['node'])

    Node = Tree('One Procedure Declaration', children)
    output["node"] = Node
    output["index"] = block_output["index"]

    return output
def Execution(pointer):
    output = dict()
    children = []

    block_output = Block(pointer)
    children.append(block_output['node'])

    dot_output = Match(TokenType.Dot , block_output['index'])
    children.append(dot_output['node'])

    Node = Tree('Execution', children)
    output["node"] = Node
    output["index"] = dot_output["index"]

    return output


def Expression(pointer):
    output = dict()
    children = []

    term_output = Term(pointer)
    children.append(term_output['node'])

    expression_prime_output = ExpressionPrime(term_output['index'])
    children.append(expression_prime_output['node'])

    Node = Tree('Expression', children)
    output["node"] = Node
    output["index"] = expression_prime_output["index"]

    return output

def ExpressionPrime(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.AddOp:
        add_op_output = Match(TokenType.AddOp , pointer)
        children.append(add_op_output['node'])

        term_output = Term(add_op_output['index'])
        children.append(term_output['node'])

        expression_prime_output = ExpressionPrime(term_output['index'])
        children.append(expression_prime_output['node'])

    elif current['type'] == TokenType.SubtractOp:
        sub_op_output = Match(TokenType.SubtractOp , pointer)
        children.append(sub_op_output['node'])

        term_output = Term(sub_op_output['index'])
        children.append(sub_op_output['node'])

        expression_prime_output = ExpressionPrime(term_output['index'])
        children.append(expression_prime_output['node'])

    else:
        expression_prime_output = None

    Node = Tree('Expression Prime', children)
    output["node"] = Node
    output["index"] = expression_prime_output["index"] if expression_prime_output else pointer

    return output

def Term(pointer):
    output = dict()
    children = []

    factor_output = Factor(pointer)
    children.append(factor_output['node'])

    term_prime_output = TermPrime(factor_output['index'])
    children.append(term_prime_output['node'])

    Node = Tree('Term', children)
    output["node"] = Node
    output["index"] = term_prime_output["index"]

    return output

def TermPrime(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.MultiplyOp:
        operator_output = Match(TokenType.MultiplyOp , pointer)
        children.append(operator_output['node'])

        factor_output = Factor(operator_output['index'])
        children.append(factor_output['node'])

        term_prime_output = TermPrime(factor_output['index'])
        children.append(term_prime_output['node'])

    elif current['type'] == TokenType.DivideOp:
        operator_output = Match(TokenType.DivideOp, pointer)
        children.append(operator_output['node'])

        factor_output = Factor(operator_output['index'])
        children.append(factor_output['node'])

        term_prime_output = TermPrime(factor_output['index'])
        children.append(term_prime_output['node'])

    else:
        term_prime_output = None

    Node = Tree('Term Prime', children)
    output["node"] = Node
    output["index"] = term_prime_output["index"] if term_prime_output else pointer

    return output

def Factor(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.Identifier:
        identifier_output = Match(TokenType.Identifier , pointer)
        children.append(identifier_output['node'])

        final_output = FactorPrime(identifier_output['index'])
        children.append(final_output['node'])

    elif current['type'] == TokenType.OpenParenthesis:
        open_parenthesis_output = Match(TokenType.OpenParenthesis , pointer)
        children.append(open_parenthesis_output['node'])

        expression_output = Expression(open_parenthesis_output['index'])
        children.append(expression_output['node'])

        final_output = Match(TokenType.CloseParenthesis , expression_output['index'])
        children.append(final_output['node'])

    else:
        final_output = Number(pointer)
        children.append(final_output['node'])

    Node = Tree('Factor', children)
    output["node"] = Node
    output["index"] = final_output["index"]

    return output

def FactorPrime(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.OpenParenthesis:
        open_parenthesis_output = Match(TokenType.OpenParenthesis, pointer)
        children.append(open_parenthesis_output['node'])

        expression_list_output = ExpressionList(open_parenthesis_output['index'])
        children.append(expression_list_output['node'])

        final_output = Match(TokenType.CloseParenthesis, expression_list_output['index'])
        children.append(final_output['node'])

    else:
        final_output = None

    Node = Tree('Factor Prime', children)
    output["node"] = Node
    output["index"] = final_output["index"] if final_output else pointer

    return output

def Number(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.IntegerConstant:
        final_output = Match(TokenType.IntegerConstant , pointer)
    else:
        final_output = Match(TokenType.RealConstant , pointer)

    children.append(final_output['node'])

    Node = Tree('Number', children)
    output["node"] = Node
    output["index"] = final_output["index"]

    return output


def ExpressionList(pointer):
    output = dict()
    children = []

    expression_output = Expression(pointer)
    children.append(expression_output['node'])

    expression_list_prime_output = ExpressionListPrime(expression_output['index'])
    children.append(expression_list_prime_output['node'])

    Node = Tree('Expression List', children)
    output["node"] = Node
    output["index"] = expression_list_prime_output["index"]

    return output

def ExpressionListPrime(pointer):
    output = dict()
    children = []

    current = Tokens[pointer].to_dict()

    if current['type'] == TokenType.Comma:
        comma_output = Match(TokenType.Comma , pointer)
        children.append(comma_output['node'])

        expression_output = Expression(comma_output['index'])
        children.append(expression_output['node'])

        expression_list_prime_output = ExpressionListPrime(expression_output['index'])
        children.append(expression_list_prime_output['node'])

    else:
        expression_list_prime_output = None

    Node = Tree('Expression List Prime', children)
    output["node"] = Node
    output["index"] = expression_list_prime_output["index"] if expression_list_prime_output else pointer

    return output


########################################################################################
def Match(current_token_type, pointer):
    output = dict()
    if pointer < len(Tokens):
        temp = Tokens[pointer].to_dict()
        if temp['type'] == current_token_type:
            pointer += 1
            output["node"] = [temp['lexeme']]
            output["index"] = pointer
            return output
        else:
            output["node"] = ["error"]
            output["index"] = pointer + 1
            errors.append("Syntax error : " + temp['lexeme'] + "Expected " + token_types_map[current_token_type] )
            return output
    else:
        output["node"] = ["error"]
        output["index"] = pointer + 1
        return output
########################################################################################