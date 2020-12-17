def is_in_range(val, r):
    return (int(r[0][0]) <= val <= int(r[0][1])) or (int(r[1][0]) <= val <= int(r[1][1]))

def valid_ticket(ticket_number, ranges):
    sum = 0
    for x in ticket_number:
        val = int(x)
        valid = False
        for r in ranges:
            in_range = is_in_range(val, r)
            if in_range:
                valid = True
                break
        if not valid:
            sum += val

    return sum

#with open("test.txt") as file:
with open("day16.txt") as file:
    data = file.readlines()
    line = 0

    ranges = []    
    while True:
        x = data[line].strip()        
        if not x:
            break
    
        parts = [rng.strip().split("-") for rng in x.split(": ")[1].split("or")]

        ranges.append((parts[0], parts[1]))
        line += 1

    line += 2
    print(data[line])

    your_tick = data[line].split(",")
    print (valid_ticket(your_tick, ranges))

    line += 3
    running_sum = 0
    valid_tickets = []
    while line < len(data):
        ticket = data[line].strip().split(",")
        invalid_values = valid_ticket(ticket, ranges)
        if (invalid_values == 0):
            assert len(ticket) == len(ranges)
            valid_tickets.append(ticket)

        running_sum += invalid_values
        line += 1

    print("Part 1", running_sum)
    #print(valid_tickets)

    # determine columns

    possible_mapping = {}

    col_index = 0

    for col_index in range(len(ranges)):
        test_range = ranges[col_index]
        mapping = {}
        for ticket in valid_tickets:
            for i in range(len(ticket)):
                if is_in_range(int(ticket[i]), test_range):
                    mapping[i] = mapping.get(i,0) + 1
        for x in mapping:
            if mapping[x] == len(valid_tickets):
                l = possible_mapping.get(col_index, [])
                l.append(x)
                print (col_index, "maps to", x)
                possible_mapping[col_index] = l

    
    real_mapping = {}
    while len(possible_mapping) > 0:
        val_found = None
        for col_index in possible_mapping:
            if len(possible_mapping[col_index]) == 1:
                val_found = possible_mapping[col_index][0]
                real_mapping[col_index] = val_found
                del possible_mapping[col_index]
                break

        for col_index in possible_mapping:
            if val_found in possible_mapping[col_index]:
                possible_mapping[col_index].remove(val_found)

        product = 1
        valid = True
        for x in [0,1,2,3,4,5]:
            if x in real_mapping:
                product *= int(your_tick[real_mapping[x]])
            else:
                valid = False
                break

        if valid:
            print("part 2", product)
    print(real_mapping)