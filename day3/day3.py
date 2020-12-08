with open("day3.txt", "rt") as file:
    data = [x.strip() for x in file.read().splitlines()]

    width = len(data[0])
    height = len(data)

    tree_counts = []
    slopes = [(3,1),(1,1),(5,1),(7,1),(1,2)]
    for offset in slopes:
        x,y = 0,0
        trees = 0
        while y < height - offset[1]:
            x += offset[0]
            y += offset[1]
            if data[y][x % width] == '#':
                trees += 1

        tree_counts.append(trees)
    
    product = 1
    for n in tree_counts:
        product *= n

    print("Part 1:",tree_counts[0])
    print("Part 2:",product)
        

    
        