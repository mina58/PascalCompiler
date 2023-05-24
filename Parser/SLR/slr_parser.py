import traceback

from Parser.Grammar.grammar import Grammar
from Scanner.token import Token
from Scanner.token_types import TokenType
from nltk.tree import Tree

class SLRParser:
    def __init__(self, grammar_file):
        self.grammar = Grammar(grammar_file)
        self.parsing_table = self.build_parsing_table()
        self.stack = []

    def build_parsing_table(self):
        self.parsing_table = {}

        # get the closure of the initial LR(0) state
        start_production = list(self.grammar.get_productions(self.grammar.start))[0]
        # we create a set of the initial state , G -> .S , 0 where 0 is the dot position
        initial_state = frozenset([(self.grammar.start, start_production, 0)])
        initial_closure = self.closure(initial_state)  # set of all possible states that can be reached from the initial state

        # print(f"Initial Closure: {initial_closure}")

        # Initialize the parsing table
        for state in initial_closure:
            self.parsing_table[state] = {}

        # Process each state in the parsing table
        for state in self.parsing_table.keys():
            for symbol in self.grammar.symbols:
                if symbol != '~':
                    # Compute the goto state
                    goto_state = self.goto(state, symbol)

                    if goto_state:
                        # Shift action
                        if symbol in self.grammar.symbols and symbol != '~':
                            self.parsing_table[state][symbol] = ('shift', goto_state)

            # Reduce action
            head = state[0]
            body = state[1]
            dot_position = state[2]
            # production is a tuple of (head, body, dot_position)
            # head -> body . , dot position at the end of the body
            if dot_position == len(body):
                # if the dot position is at the end of the body means that we have reached the end of the production
                # accept action

                for follow_symbol in self.follow(head):
                    if follow_symbol in self.parsing_table[state]:
                        # if the follow symbol is already in the parsing table
                        # Conflict check: ensure no shift-reduce or reduce-reduce conflicts
                        existing_action = self.parsing_table[state][follow_symbol]
                        if existing_action[0] != 'reduce' or existing_action[1] != (head, body, dot_position):
                            # if the existing action is not reduce or the existing action is not the same as the current production
                            # then we have a conflict
                            raise Exception(f'Conflict in state {state} for symbol {follow_symbol}.')
                        else:
                            continue
                    # Reduce action
                    self.parsing_table[state][follow_symbol] = ('reduce', (head, body, dot_position))

        # print(f"Parsing Table: {self.parsing_table}")

        # handle the accept action
        if self.grammar.start in self.parsing_table and '$' in self.parsing_table[self.grammar.start]:
            # if the start symbol is in the parsing table and the end of input symbol is in the parsing table
            # then we have an accept action
            self.parsing_table[self.grammar.start]['$'] = ('accept', None)
        return self.parsing_table

    def closure(self, state):
        #return the closure of the given state ; all possible states that can be reached from the given state
        closure = set(state)

        while True:
            new_items = set()

            for item in closure:
                head, body, dot_position = item

                if dot_position < len(body) and body[dot_position] in self.grammar.non_terminals:
                    next_symbol = body[dot_position]
                    productions = self.grammar.get_productions(next_symbol)

                    for production in productions:
                        new_item = (next_symbol, production, 0)

                        if new_item not in closure:
                            new_items.add(new_item)

            if not new_items:
                break

            closure.update(new_items)

        return closure

    def goto(self, state, symbol):
        goto_state = set()

        if state[2] < len(state[1]) and state[1][state[2]] == symbol:
            #where state[2] is the dot position and state[1] is the body and state[1][state[2]] is the symbol at the dot position
            # Shift the dot position by one to indicate that we have processed the symbol
            # #and explore the state that can be reached from the current state based on the symbol
            new_item = (state[0], state[1], state[2] + 1)
            goto_state.add(new_item)

        return self.closure(goto_state)

    def follow(self, symbol):
        follow_set = set()

        for head, bodies in self.grammar.grammar.items():
            #head is the non terminal symbol and bodies is a set of all the productions of the non terminal symbol
            for body in bodies:
                for i, item in enumerate(body):
                    if item == symbol:
                        if i == len(body) - 1:
                            #if the symbol is the last symbol in the body then we add the follow set of the head
                            if head != symbol:
                                follow_set.update(self.follow(head))
                        else:
                            follow_set.update(self.first(body[i + 1:]))

        return follow_set

    def first(self, symbols):
        first_set = set()

        for symbol in symbols:
            if symbol in self.grammar.terminals:
                first_set.add(symbol)
                break

            #else if the symbol is a non terminal symbol
            first_set.update(self.first(self.grammar.get_productions(symbol)))

            if '~' not in first_set:
                #if we have epsilon in the first set then we continue to the next symbol
                break

        return first_set

    def parse(self, tokens):
        self.stack = [0]
        tokens.append(Token('$', TokenType.EOF))

        pointer = 0  # pointer to the current token

        # create the parse tree
        parse_tree = Tree('Program', [])

        try:
            while True:
                state = self.stack[-1]  # FILO mode
                current_token = tokens[pointer].as_dict()
                action = self.parsing_table[state].get(current_token['type'], None)
                # get the action from the parsing table by the current state and the current token
                # action is a tuple of (action_type, action_value)

                # print(f"Current token: {current_token['lexeme']}")
                # print(f"Current state: {state}")
                # print(f"Action: {action}")

                if not action:
                    raise Exception(f'Unexpected token {current_token["lexeme"]} at index {pointer}.')

                action_type, action_value = action
                # action_type is either shift, reduce, or accept
                # action_value is the state to shift to or the production to reduce or None indicating accept

                if action_type == 'shift':
                    # shift the current token to the stack and move the pointer to the next token
                    self.stack.append(action_value)
                    pointer += 1

                elif action_type == 'reduce':
                    head, body, dot_position = action_value
                    for _ in range(len(body)):
                        self.stack.pop()

                    state = self.stack[-1]  # we get the state after popping the body

                    self.stack.append(self.parsing_table[state][head][1])
                    # we get the state to shift to after reducing the body where state is the current state
                    # and head is the non-terminal symbol
                    # and [1] is the action value which is the state to shift to

                    # create a node in the parse tree for the reduced non-terminal symbol
                    non_terminal_node = Tree(head, [])
                    child_nodes = []

                    for _ in range(len(body)):
                        child_nodes.append(parse_tree.pop())

                    child_nodes.reverse()
                    non_terminal_node.extend(child_nodes)
                    parse_tree.append(non_terminal_node)

                elif action_type == 'accept':
                    print('Accepted.')
                    break
                else:
                    raise Exception(f'Unknown action type {action_type}.')

                if pointer >= len(tokens):
                    raise Exception('Unexpected end of input.')

                # print(f"Stack: {self.stack}")

        except Exception as e:
            #print traceback
            traceback.print_exc()
            print(f"Exception occurred during parsing: {e}")

        return parse_tree

