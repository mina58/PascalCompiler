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
                self.grammar[head] = self.grammar.get(head, set())

                self.non_terminals.add(head)

                bodies = [body.split() for body in bodies.split(' | ')]

                #now check that ~ only exists alone in the body and if not assert it does not exist
                for body in bodies:
                    if len(body) == 1 and body[0] == '~':
                        continue
                    for symbol in body:
                        #assert that ~ doesnt exist in the body
                        assert symbol != '~', f'\'~\' is not a valid terminal symbol.'
                        if symbol[0].isupper():
                            self.non_terminals.add(symbol)
                        else:
                            self.terminals.add(symbol)
                    self.grammar[head].add(tuple(body))

            #now add terminals and non terminals to symbols
            self.symbols = self.terminals.union(self.non_terminals)




