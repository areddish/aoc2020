with open("day3.txt", "rt") as file:
    data = file.readlines()

    width = len(data[0])
    height = len(data)

    print (width,height)
    board = []
    for d in range(height):
        board.append(data[d].strip() * 8 * 15)

    tree_counts = []
    slopes = [(3,1),(1,1),(5,1),(7,1),(1,2)]
    for offset in slopes:
        x,y = 0,0
        trees = 0
        while y < height - offset[1]:
            x += offset[0]
            y += offset[1]
            if board[y][x] == '#':
                trees += 1

        tree_counts.append(trees)
    
    product = 1
    for n in tree_counts:
        product *= n

    print("Part 1:",tree_counts[0])
    print("Part 2:",product)
    # print (width, height)
    # trees = 0
    # start = (0,0)
    # while start[1] < len(data)-1:        
    #     start = (move(start[0], width), start[1] + 1)        
    #     print (start)
    #     print(data[start[1]][start[0]])
    #     if (data[start[1]][start[0]] == '#'):
    #         trees += 1
        

    
        