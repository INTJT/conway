class Rule:

    def __init__(self, born, survive):
        if not all([b in range(9) for b in born]) or not all([s in range(9) for s in survive]):
            raise ValueError("The count of living adjacent cells must be in range from 0 to 8")
        self.born, self.survive = tuple(set(born)), tuple(set(survive))

    @property
    def bs_notation(self):
        return f"B{''.join([str(b) for b in self.born])}/S{''.join([str(s) for s in self.survive])}"

    def __repr__(self): return self.bs_notation

    @staticmethod
    def from_bs_notation(bs):

        try:

            b, s = [s.replace(' ', '') for s in bs.upper().split('/')]
            
            if b[0] != 'B' or s[0] != 'S':
                raise Exception()

            b_numbers = [int(b) for b in b[1:]]
            s_numbers = [int(s) for s in s[1:]]

            return Rule(b_numbers, s_numbers)

        except Exception:

            raise ValueError("Invalid B/S notation")
