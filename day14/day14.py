def num_to_bit_vec(length, val):
    result =[]
    for x in range(length):
        # Test bit, if set add one
        if val & (1 << x):
            result.append(1)
        else:
            result.append(0)

    return result

def set_bit(v, bit, val):
    if val == 1:
        v |= (1 << bit)
    else:
        v &= ~(1 << bit)
    return v

def mem_locations(mask, b):
    bit = 1
    assert len(mask) == 36

    floating_index = []
    for x in range(35,-1,-1):
        if mask[x] == "1":
            b |= bit
        elif mask[x] == "0":
            pass #unchanged
        elif mask[x] == "X":
            floating_index.append(x)
        bit *= 2
    
    if floating_index:
        address = []
        val = 0
        while (val < pow(2,len(floating_index))):
            copy = b
            vec = num_to_bit_vec(len(floating_index), val)
            for pairs in list(zip(floating_index, vec)):
                copy = set_bit(copy, 35-pairs[0], pairs[1])
            address.append(copy)
            val += 1
        return address
    else:
        return [b]

def mask_value(mask, b):
    bit = 1
    assert len(mask) == 36
    assert 0 <= b <= pow(2, 36)

    for x in range(35,-1,-1):
        if mask[x] == "1":
            b |= bit
        elif mask[x] == "0":
            b &= ~bit
        bit *= 2
    assert bit == pow(2,36)
    assert 0 <= b <= pow(2, 36)
    return b

#with open("test2.txt", "rt") as file:
with open("day14.txt", "rt") as file:
    data = [x for x in file.read().splitlines()]

    instr = []
    mem_len = len(data)
    for x in data:
        parts = x.split(' ')
        assert len(parts) == 3
        if "mask" in parts[0]:
            instr.append((-1, parts[2].strip()))
        else:
            index = int(parts[0].replace("mem[","").replace("]", ""))
            val = int(parts[2])
            instr.append((index, val))
            mem_len = max(mem_len, index)

    mask = instr[0][1]
    mem = [0] * (mem_len + 1)
    for x in instr:
        if x[0] == -1:
            mask = x[1]
        else:
            mem[x[0]] = mask_value(mask, x[1])

    print("Part 1", sum(mem))

    ## Part 2
    mask = instr[0][1]
    f = {}
    for x in instr:
        if x[0] == -1:
            mask = x[1]
        else:
            for address in mem_locations(mask, x[0]):
                f[address] = x[1]
    
    # 22998646173
    print("Part 2", sum([f[x] for x in f]))
