import math
from PIL import Image

RIGHT = 1
BOTTOM = 2
LEFT = 3
TOP = 4

def write_image(image, tiles, ids):
    y_max = len(tiles[ids[0]].grid)
    assert y_max == 10
    # Skip first and last row
    for y in range(1,y_max-1):
        row = []            
        for i in ids:
            tile = tiles[i]
            # Skip first and last col
            assert len(tile.grid[y]) == 10
            row += tile.grid[y][1:-1]                
        image.append(row)


def flip(data, horiztonal=True):
    data_copy = []
    if horiztonal:
        for y in data:
            row = []
            for x in y:
                row.insert(0,x)
            data_copy.append(row)
    else:
        for y in data:
            data_copy.insert(0,y)
    return data_copy

def rotate(data):
    return [list(x) for x in zip(*data[::-1])]

class Tile:
    def __init__(self, id, data):
        self.grid = data
        self.id = id

    def edge_number(self, which, reverse=False):
        if which == TOP:
            edge = self.grid[0][:]
        elif which == BOTTOM:
            edge = list(reversed(self.grid[-1][:]))
        else:
            edge = []
            for y in range(len(self.grid)):
                edge.append(self.grid[y][0] if which == LEFT else self.grid[y][-1])
            if which == LEFT:
                edge = list(reversed(edge))

        if reverse:
            edge = list(reversed(edge))

        return sum([(2 << i) if ch == "#" else 0 for i, ch in enumerate(edge)])

    def find_edges(self):
        top = self.grid[0][:]
        bottom = list(reversed(self.grid[-1][:]))
        left = []
        right = []
        for y in range(len(self.grid)):
            left.append(self.grid[y][0])
            right.append(self.grid[y][-1])

        left = list(reversed(left))
        t = [sum([(2 << i) if ch == "#" else 0 for i, ch in enumerate(top)]), sum([(2 << i) if ch == "#" else 0 for i, ch in enumerate(reversed(top))])]
        b = [sum([(2 << i) if ch == "#" else 0 for i, ch in enumerate(bottom)]), sum([(2 << i) if ch == "#" else 0 for i, ch in enumerate(reversed(bottom))])]
        l = [sum([(2 << i) if ch == "#" else 0 for i, ch in enumerate(left)]), sum([(2 << i) if ch == "#" else 0 for i, ch in enumerate(reversed(left))])]
        r = [sum([(2 << i) if ch == "#" else 0 for i, ch in enumerate(right)]), sum([(2 << i) if ch == "#" else 0 for i, ch in enumerate(reversed(right))])]

        return self.id, t, b, l, r

    def orient(self, connected_id, dir):
        _, t, b, l, r = self.find_edges()            
        # Top is opposite orientation from bottom
        # ---> Top
        # <--- bottom
        # if connected_id == t[1]:
            # return

        # If we are not in the current orientation, we need to flip first
        if connected_id not in [t[1],b[1],l[1],r[1]]:            
            if connected_id == r[0]:
                self.rot()
                self.rot()
                self.rot()
                self.flip_horizontal()
            elif connected_id == l[0]:
                self.flip_vertical()
                self.rot()
            else:
                assert connected_id == t[0] or connected_id == b[0]
                self.flip_horizontal()

        # Now rotate into position
        while connected_id != self.edge_number(dir, reverse=True):
            self.rot()

    def flip_horizontal(self):
        self.grid = flip(self.grid, horiztonal=True)

    def flip_vertical(self):
        self.grid = flip(self.grid, horiztonal=False)

    def rot(self):
        self.grid = rotate(self.grid)

    def print(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                print(self.grid[y][x], end="")
            print()

#with open("test.txt") as file:
with open("day20.txt") as file:
    data = file.read().splitlines()

    tiles = {}
    i = 0
    while i < len(data):
        tile_id = int(data[i].split(" ")[1].split(":")[0])
        i += 1
        print(tile_id)

        tile_data = []
        while i < len(data) and data[i]:
            # read tile
            tile_data.append(list(data[i]))
            i+=1

        tiles[tile_id] = Tile(tile_id, tile_data)
        i+=1

    print(len(tiles))
    nodes = {}
    for tile in tiles:
        id, t, b, l, r = tiles[tile].find_edges()
        nodes[t[0]] = nodes.get(t[0], []) + [tiles[tile].id]
        nodes[b[0]] = nodes.get(b[0], []) + [tiles[tile].id]
        nodes[l[0]] = nodes.get(l[0], []) + [tiles[tile].id]
        nodes[r[0]] = nodes.get(r[0], []) + [tiles[tile].id]
        nodes[t[1]] = nodes.get(t[1], []) + [tiles[tile].id]
        nodes[b[1]] = nodes.get(b[1], []) + [tiles[tile].id]
        nodes[l[1]] = nodes.get(l[1], []) + [tiles[tile].id]
        nodes[r[1]] = nodes.get(r[1], []) + [tiles[tile].id]

    paired_nodes = {}
    for n in nodes:
        if len(nodes[n]) == 2:
            paired_nodes[n] = True

    corners = []
    for tile in tiles:
        id, t, b, l, r = tiles[tile].find_edges()
        if t[0] not in paired_nodes and t[1] not in paired_nodes and l[0] not in paired_nodes and l[1] not in paired_nodes:
            print("upper left is ", id)
            corners.append(id)
        elif t[0] not in paired_nodes and t[1] not in paired_nodes and r[0] not in paired_nodes and r[1] not in paired_nodes:
            print("upper right is ", id)
            corners.append(id)
        elif b[0] not in paired_nodes and b[1] not in paired_nodes and l[0] not in paired_nodes and l[1] not in paired_nodes:
            print("lower left is ", id)
            corners.append(id)
        elif b[0] not in paired_nodes and b[1] not in paired_nodes and r[0] not in paired_nodes and r[1] not in paired_nodes:
            print("lower right is ", id)
            corners.append(id)

    print("Part 1", corners[0] * corners[1] * corners[2] * corners[3])

    upper_left = None
    # Start in the upper left corner
    for c in corners:
        top = tiles[c].edge_number(TOP)
        left = tiles[c].edge_number(LEFT)
        if len(nodes[top]) == 1 and nodes[top][0] == c and len(nodes[left]) == 1 and nodes[left][0] == c:
            upper_left = tiles[c]
            break
    assert upper_left

    current = upper_left
    width = math.sqrt(len(tiles))

    image = []
    y = 0
    while y < width:
        current = upper_left
        # Move DOWN y times
        direction = BOTTOM
        for _ in range(y):
            edge_id = tiles[current.id].edge_number(direction)
            next_tile_id = nodes[edge_id][0] if nodes[edge_id][0] != current.id else nodes[edge_id][1]
            next_tile = tiles[next_tile_id]
            next_tile.orient(edge_id, TOP)
            #write_image(piece, image)
            current = next_tile

        # fill in a row        
        pieces = 0
        direction = RIGHT
        ids = []
        print(" " + str(current.id) +" ", end="")
        while pieces < width - 1:
            ids.append(current.id)

            edge_id = tiles[current.id].edge_number(direction)
            next_tile_id = nodes[edge_id][0] if nodes[edge_id][0] != current.id else nodes[edge_id][1]
            next_tile = tiles[next_tile_id]
            next_tile.orient(edge_id, LEFT if direction == RIGHT else RIGHT)

            print(" " + str(next_tile.id) +" ", end="")
            #write_image(piece, image)
            current = next_tile
            pieces += 1
        print()

        ids.append(current.id)
        write_image(image, tiles, ids)
        y += 1

    # im = Image.new(mode="RGB", size = (len(image[0]), len(image)))
    # pix = im.load()
    # for y in range(len(image)):
    #     for x in range(len(image[0])):
    #         print(image[y][x], end="")
    #         pix[x,y] = (255,0,0) if image[y][x] == "#" else (0,0,0)
    #     print()
    # im.show()

    frames = []
    def addFrame(image, mag=4):
        im = Image.new(mode="RGB", size = (len(image[0])*mag, len(image)*mag))
        pix = im.load()
        for y in range(len(image)):
            for x in range(len(image[0])):
                color = (11,16,87)
                if image[y][x] == "#":
                    color= (72,47,228)
                elif image[y][x] == "O":
                    color = (255,255,0)
                elif image[y][x] == "x":
                    color = (181,230,29)
                for wx in range(mag):
                    for wy in range(mag):
                        pix[(x*mag)+wx,(y*mag)+wy] = color
        return im
    frames.append(addFrame(image))


    # find seamonsters
    #if none found, flip horiz

    # scan for seamonster
    #            1111111111
    #   01234567890123456789
    #  0                  # 
    #  1#    ##    ##    ###
    #  2 #  #  #  #  #  #   
    seamonster_offset = [(18,0), (0,1), (5,1), (6,1), (11,1), (12,1), (17,1), (18,1), (19,1), (1,2), (4,2), (7,2), (10,2), (13,2), (16,2)]
    seamonsters_found = 0
    op = [rotate, rotate, rotate, rotate, flip, rotate, rotate, rotate, rotate, lambda x: flip(x,horiztonal=False), rotate, rotate, rotate, rotate ]
    op_index = 0
    while seamonsters_found == 0:
        for y in range(len(image) - 3):
            for x in range(len(image[0]) - 19):
                is_sea_monster = True
                for offset in seamonster_offset:
                    dx,dy = offset
                    if image[dy+y][dx+x]!= "#":
                        is_sea_monster = False
                        break
                if is_sea_monster:
                    seamonsters_found += 1
                    for offset in seamonster_offset:
                        dx,dy = offset
                        image[dy+y][x+dx] = "O"
                    frame = addFrame(image)
                    frames.append(frame)
                    frames.append(frame)
                    frames.append(frame)
        if seamonsters_found == 0:
            image = op[op_index](image)
            op_index+=1
        frame = addFrame(image)
        frames.append(frame)
        frames.append(frame)
        frames.append(frame)

    frames[0].save("test.gif", format="GIF", append_images=frames[1:], save_all=True, duration=50, loop=0, optimize=True, quality=10)

    count = 0
    for y in range(len(image)):
        for x in range(len(image[0])):
            if image[y][x] == "#":
                count += 1
    print ("part 2", count)