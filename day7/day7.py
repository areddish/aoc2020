def can_hold_shiny(c, mapping):
    for holds in mapping[c]:
            if holds[1] == "shiny gold" or can_hold_shiny(holds[1], mapping):
                return True
    return False

def bags_in(color, mapping):       
    count = 0
    for bags in mapping[color]:
        count += bags[0] + bags[0] * bags_in(bags[1], mapping)
    return count

#with open("test.txt", "rt") as file:
#with open("test2.txt", "rt") as file:
with open("day7.txt", "rt") as file:
    data = file.read().splitlines()

    mapping = {}
    for line in data:
        parts = line.split(" ")
        color = parts[0] + " " + parts[1]
        assert parts[2] == "bags"
        assert parts[3] == "contain"
        x = 4
        bags_contained = []
        if parts[x] != "no":
            while x < len(parts):
                count = int(parts[x])
                bag = parts[x+1] + " " + parts[x+2]
                # print (f"{count} {bag}")
                bags_contained.append((count, bag))
                x += 4
        # if parts[4] == no this will be empty
        mapping[color] = bags_contained

    can_hold = 0
    for bag_color in mapping:
        if (can_hold_shiny(bag_color, mapping)):
            can_hold += 1

    print ("Part 1", can_hold)

    bag_count = 0
    for bag_info in mapping["shiny gold"]:
        bag_count += bag_info[0] + bag_info[0] * bags_in(bag_info[1], mapping)
    
    print ("Part 2", bag_count)

        
        

