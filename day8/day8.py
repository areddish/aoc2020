def rewrite(op):
    if op == "nop":
        return "jmp"
    elif op == "jmp":
        return "nop"
    return op

def run_program(instructions):
    acc = 0
    prev_acc = 0
    ip = 0
    ip_processed = set()
    while ip < len(instructions) :
        if (ip in ip_processed):
            return prev_acc, ip

        ip_processed.add(ip)
        op, arg = instructions[ip]
        if op == "acc":
            acc += arg
            ip += 1
        elif op == "jmp":
            ip = ip + arg
        elif op == "nop":
            ip += 1

        prev_acc = acc

    return acc, ip

#with open("test.txt", "rt") as file:
with open("day8.txt", "rt") as file:
    data = file.read().splitlines()

    ins = []
    for x in data:
        p = x.split(" ")
        op = p[0]
        arg = int(p[1])
        ins.append((op, arg))

    print("Part 1", run_program(ins)[0])
    looped_ip = 0
    last_changed = -1
    changed = 0
    result = None
    while looped_ip < len(ins) - 1:
        result, looped_ip = run_program(ins)
        # didn't complete
        if looped_ip < len(ins):
            # restore
            if (last_changed != -1):
                ins[last_changed] = (rewrite(ins[last_changed][0]), ins[last_changed][1])
                changed = last_changed + 1

            # find the next nop/jmp and change it
            while(changed < len(ins)):
                change = rewrite(ins[changed][0])
                if change != ins[changed][0]:
                    ins[changed] = (change, ins[changed][1])
                    last_changed = changed
                    break
                changed += 1

    print("Part 2", result)