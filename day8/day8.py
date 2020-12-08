#with open("test.txt", "rt") as file:
with open("day8.txt", "rt") as file:
    data = file.read().splitlines()

    ins = []
    for x in data:
        p = x.split(" ")
        op = p[0]
        arg = int(p[1])
        ins.append((op, arg))

    acc = 0
    prevacc = 0
    ip = 0
    seen = set()
    while (ip < len(ins)):
        if (ip in seen):
            print ("part 1", prevacc)
            break

        seen.add(ip)
        op, arg = ins[ip]
        if op == "acc":
            acc += arg
            ip += 1
        elif op == "jmp":
            ip = ip + arg
        elif op == "nop":
            ip += 1

        prevacc = acc
        
    def toggle(i):
        if i == "nop":
            return "jmp"
        elif i == "jmp":
            return "nop"
        return i

    # part 2
    acc = 0
    ip = 0
    seen = set()
    last_changed = -1
    changed = 0
    while (ip < len(ins)):
        while (ip < len(ins)):
            if (ip in seen):
                # restore
                if (last_changed != -1):
                    ins[last_changed] = (toggle(ins[last_changed][0]), ins[last_changed][1])
                    changed = last_changed + 1

                # find the first nop/jmp and change it
                while(changed < len(ins)):
                    change = toggle(ins[changed][0])
                    if change != ins[changed][0]:
                        ins[changed] = (change, ins[changed][1])
                        last_changed = changed
                        break
                    changed += 1

                ip = 0
                seen = set()
                acc = 0
            else:
                seen.add(ip)
                op, arg = ins[ip]
                if op == "acc":
                    acc += arg
                    ip += 1
                elif op == "jmp":
                    ip = ip + arg
                elif op == "nop":
                    ip += 1
        print("Part 2", acc)