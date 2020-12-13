#with open("test.txt", "rt") as file:
with open("day13.txt", "rt") as file:
    data = [x for x in file.read().splitlines()]

    earliest = int(data[0])
    buses = []
    offset = -1
    for b in data[1].split(","):
        offset += 1
        if b == "x":
            continue
        buses.append((int(b), offset))
        
    # Part 1
    t = earliest
    keep_going = True
    while keep_going:
        for b in buses:
            if t % b[0] == 0:
                print ("Part 1", (t-earliest)*b[0])
                keep_going = False
                break
        t += 1
    
    num_buses = len(buses)
    # Increment
    dt = buses[0][0]
    # Bus 0 is solved, solve for the next bus (bus 1)
    bus = 1
    # could also start at 100000000000000, but it's fast enough
    t = 0   
    previous_t = None
    while (bus < num_buses ):
        # Find the next t where the bus we're looking at has a solution
        while (t+buses[bus][1]) % buses[bus][0] != 0:
            t += dt

        assert t % buses[0][0]== 0

        # If we are at the last bus, we are done and can ust print the time.
        if bus == num_buses - 1:
            print ("Part 2", t)
            break

        # If we have a previous time, compute the new delta and move onto the next
        # bus. The rate of change of time continues to increase based on the assumption
        # the pattern repeats, which was discovered empirically.
        if previous_t:
            dt = t - previous_t
            previous_t = None
            bus += 1    # Move to the next bus
        else:
            # Otherwise we are going to look for another occurence to detect/measure the pattern
            # Assumption the goal state doesn't occur before the pattern develops.
            previous_t = t
        t += dt