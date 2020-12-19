import re
import copy

def build_expr(rules, rule, part2=True):
    expr = ""
    for x in rule:
        if isinstance(rules[x], list):
            if isinstance(rules[x][0], list):
                sep = ""
                expr += "("
                for i in rules[x]:
                    expr += sep
                    expr += build_expr(rules, i, part2)
                    sep = "|"
                expr += ")"
            else:
                expr += build_expr(rules, rules[x], part2)
                # 42 | 42 8 => 42+
                if part2 and x == "8":
                    expr += "+"
        else:
            assert isinstance(rules[x], str)
            expr += rules[x]

    return expr

#with open("test2.txt") as file:
with open("day19.txt") as file:
    data = file.read().splitlines()
    
    rules = {}
    load_rules = True
    letters = {}
    messages = []
    for x in data:
        if load_rules:
            if not x:
                load_rules = False
                continue

            p = x.split(":")
            rule_number = p[0]
            if "|" in x:
                sub_rules = []
                for x in p[1].split("|"):
                    sub_rules.append(x.strip().split(" "))
                rules[rule_number] = sub_rules
            elif "\"" in x:
                ch = p[1].replace("\"", "").strip()
                rules[rule_number] = ch
                letters[rule_number] = ch
            else:
                rules[rule_number] = p[1].strip().split(" ")
        else:
            messages.append(x)
        

    #print(rules)
    expr = build_expr(rules, rules["0"], part2=False)
    count = 0
    for msg in messages:
        if re.fullmatch(expr, msg):        
            #print(msg)
            count += 1
    print("part 1", count)

    # hack, expand out the rule some number of times
    # 11: 42 31 | 42 11 31 
    # Means 42 (42 31) 31 or 42 42 42 31 31 31
    rules["11"] = [ ["42"]*n + ["31"]*n for n in range(1,5)]
    count = 0
    expr = build_expr(rules, "0", part2=True)
    for msg in messages:
        if re.fullmatch(expr, msg):
            #print (msg)
            count += 1
    print ("part 2", count)

    
    