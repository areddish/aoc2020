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

    program = []
    for x in data:
        op, arg_str = x.split(" ")
        program.append((op, int(arg_str)))

    print("Part 1", run_program(program)[0])
    looped_ip = 0
    last_changed = -1
    changed = 0
    result = None
    while looped_ip < len(program):
        result, looped_ip = run_program(program)
        # didn't complete
        if looped_ip < len(program):
            # Reverse last rewrite, if done
            if (last_changed != -1):
                program[last_changed] = (rewrite(program[last_changed][0]), program[last_changed][1])
                changed = last_changed + 1

            # Find the next rewrite candidate and then try again
            while(changed < len(program)):
                change = rewrite(program[changed][0])
                if change != program[changed][0]:
                    program[changed] = (change, program[changed][1])
                    last_changed = changed
                    break
                changed += 1

    print("Part 2", result)