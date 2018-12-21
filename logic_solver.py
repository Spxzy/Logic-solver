class rule:
    def __init__(self, input, output):
        self.input = input
        self.output = output

    def applyTo(self, query):
        query = query.replace(" ", "")
        input = self.input.replace(" ", "")
        print(get_variables(query, input))
        #query = self.output
        #for var in variables:
        #    query = query.replace(var, variables[var])

        return query

def get_variables(query, input):
    variables = {}
    parentheses = 0
    str = ""
    for char in query:
        if char in "[(":
            parentheses += 1
            str += char
        elif char in "])":
            parentheses -= 1
            str += char
        elif char in LOGIC_OPERATORS and not parentheses:
            var_name = ""
            for i_char in input:
                if i_char == char:
                    if str:
                        variables[var_name] = str
                    var_name = ""
                elif input.index(i_char) == len(input) - 1:
                    var_name += i_char
                    variables[var_name] = query.replace(str + char, "")
                else:
                    var_name += i_char
            str = ""
        else:
            str += char
    return variables


RULES = {'negation_normal_form': (rule("A ↔ B", "(¬A ∨ B) ∧ (A ∨ ¬B)"),
                                  rule("A → B", "¬A ∨ B"),
                                  rule("¬¬A", "A"))}
ALPHABET = "abcdefghijklmopqrstuvwxyz"
LOGIC_OPERATORS = "¬∧∨→↔"
query = "(p ∨ q) → (p ∧ q)"

print(get_variables(query.replace(" ",""), RULES["negation_normal_form"][1].input.replace(" ","")))

def match(query, rule):
    input = rule.input.replace(" ", "")
    query = query.replace(" ", "")

    for q_char, i_char in zip(query, input):
        if q_char != i_char and i_char not in ALPHABET.upper():
            return False
    return True

def to_nnf(query):
    for rule in RULES["negation_normal_form"]:
        if match(query, rule):
            query = rule.applyTo(query)
    return query

print(to_nnf(query))
