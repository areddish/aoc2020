# Parse the expression into a list of terms. Grouping parens
# into their own list of terms.
def parse(line):
    terms = []
    i = 0
    while i < len(line):
        ch = line[i]
        i += 1
        if ch == " ":
            continue
        
        # If we see an opening paren then we will greedly grab
        # as much of the expr as possible. Then recursively parse
        # that expr.
        if ch == "(":
            count = 1
            start = i - 1
            while count > 0:
                ch = line[i]
                if ch == "(":
                    count += 1
                if ch == ")":
                    count -= 1
                i += 1
            terms.append(parse(line[start+1:i-1]))
        else:
            terms.append(ch)
    return terms

# A term is either a number or an expression (sub list)
def eval_term(term, eval_eq_fn):
    if isinstance(term, list):
        return eval_eq_fn(term)
    return int(term)

def eval_part1(terms):    
    running_value = 0
    running_value = eval_term(terms.pop(0), eval_part1)
    while len(terms) > 0:        
        op = terms.pop(0)
        val2 = eval_term(terms.pop(0), eval_part1)
        if op == "*":
            running_value *= val2
        else:
            assert op == "+"
            running_value += val2
    return running_value
    
def eval_part2(terms):
    # first combine +'s
    reduced = [eval_term(terms.pop(0), eval_part2)]
    while len(terms):
        op = terms.pop(0)
        val2 = eval_term(terms.pop(0), eval_part2)
        if op == "+":
            reduced[-1] = reduced[-1] + val2
        else:
            reduced.append(op)
            reduced.append(val2)

    running_value = eval_term(reduced.pop(0), eval_part2)
    while len(reduced) > 0:        
        op = reduced.pop(0)
        val2 = eval_term(reduced.pop(0), eval_part2)
        running_value *= val2
    return running_value

with open("day18.txt") as file:
    data = file.read().splitlines()

    sum = 0
    sum2 = 0
    for line in data:
        eq = parse(line)
        sum += eval_part1(eq)
        eq = parse(line)
        sum2 += eval_part2(eq)
    
    print("Part 1", sum)
    print("Part 2", sum2)