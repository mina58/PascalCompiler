class Grammar:
    def __init__(self, grammar_file):
        self.grammar = {}
        self.start = None
        self.terminals = set()
        self.non_terminals = set()

        with open(grammar_file, 'r') as file:
            for production in file:
                production = production.strip()

                head, _, bodies = production.partition(' -> ')

                assert head[0].isupper(), f'\'{head}\' is not a valid non-terminal symbol.'

                if not self.start:
                    self.start = head

                #make sure that head exists in the grammar , if not initialize it with empty set
                if head not in self.grammar:
                    self.grammar[head] = set()

                self.non_terminals.add(head)

                bodies = [body.split() for body in bodies.split(' | ')]

                #now check that ~ only exists alone in the body and if not assert it does not exist
                for body in bodies:
                    for symbol in body:
                        #assert that ~ not in symbol in the body
                        if len(body) > 1:
                            assert '~' not in body, f'\'~\' is not a valid symbol in the body of a production rule.'
                        if symbol[0].isupper():
                            self.non_terminals.add(symbol)
                        else:
                            self.terminals.add(symbol)

                    self.grammar[head].add(tuple(body))

            #now add terminals and non terminals to symbols
            self.symbols = self.terminals.union(self.non_terminals)

        #now check that all non terminals have at least one production rule
        for non_terminal in self.non_terminals:
            assert non_terminal in self.grammar, f'\'{non_terminal}\' is not a valid non-terminal symbol.'

        #now check that no duplicate production rules exist
        for non_terminal in self.grammar:
            assert len(self.grammar[non_terminal]) == len(set(self.grammar[non_terminal])), f'Duplicate production rules exist for \'{non_terminal}\'.'

    def get_productions(self, non_terminal):
        return self.grammar[non_terminal]
