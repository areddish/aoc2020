with open("day21.txt") as file:
    data = file.read().splitlines()

    mapping = {}
    allergen_sets = {}
    for l in data:
        parts = l.split(" (contains")
        ings = parts[0].strip().split(" ")
        contains = tuple(parts[1].strip().replace(")", "").replace(",", "").split(" "))
        mapping[contains] = mapping.get(contains, []) + ings
        for allergen in contains:
            if allergen in allergen_sets:
                allergen_sets[allergen] &= set(ings)
            else:
                allergen_sets[allergen] = set(ings)

    allergen_mapping = {}
    done = False
    while not done:
        done = True
        singles = []
        for x in allergen_sets:
            if len(allergen_sets[x]) == 1:
                singles.append(x)

        for x in singles:   
            done = False     
            ingredient = allergen_sets[x].pop()
            allergen_mapping[ingredient] = x
            for y in allergen_sets:
                if ingredient in allergen_sets[y]:
                    allergen_sets[y].remove(ingredient)                
            
    count = 0
    for l in data:
        parts = l.split(" (contains")
        ings = parts[0].strip().split(" ")
        for i in ings:
            if i not in allergen_mapping:
                count += 1
    print("Part 1", count)

    print("Part 2", ",".join(sorted(allergen_mapping, key=lambda i: allergen_mapping[i])))