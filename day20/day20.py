import copy
import math
from PIL import Image

RIGHT = 1
BOTTOM = 2
LEFT = 3
TOP = 4

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
    return list(zip(*data[::-1]))    

class Tile:
    def __init__(self, id, data):
        self.grid = data
        self.id = id
        self.fixed = False
        self.rotation_locked = False
        self.manip = 0
        self.match = [0,0,0,0,0]
        self.i = 0

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

    def print_edges(self):
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
        # If we are oriented, ignore
        # flip_status = 0
        if dir == LEFT:
            if  connected_id == self.edge_number(dir):
                return
            _, t, b, l, r = self.print_edges()

            # If we are not in the current orientation, we need to flip first
            if connected_id not in [t[0],b[0],l[0],r[0]]:            
                if connected_id == r[1]:
                    self.rot()
                    self.rot()
                    self.flip_vertical()
                elif connected_id == l[1]:
                    self.flip_vertical()
                else:
                    assert connected_id == t[1] or connected_id == b[1]
                    self.flip_horizontal()
                    

            # Now rotate into position
            while connected_id != self.edge_number(dir):
                self.rot()
            return
        elif dir == TOP:
            _, t, b, l, r = self.print_edges()            
            # Top is opposite orientaion from bottom
            # ---> Top
            # <--- bottom
            if connected_id == t[1]:
                return

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
            return
                # if flip_status == 0:
                #     self.flip_horizontal()
                #     flip_status += 1
                # else:
                #     self.flip_vertical()
            
    def flip_chain(self, tiles, flipped={}, horiz=True, ):
        if len(flipped) > 0:
            flipped.add(self.id)
            if horiz:
                self.flip_horizontal()
            else:
                self.flip_vertical()
            for x in self.match:
                if x == 0 or x in flipped:
                    continue
                tiles[x].flip_chain(tiles, flipped, horiz)
        else:
            # If we are matched on the left or right we flip horiz
            if self.match[LEFT]:
                if self.match[RIGHT] or self.match[TOP] or self.match[BOTTOM]:
                    return
                self.fixed = False
                self.i += 1
                if self.i % 2 == 1:
                    self.flip_vertical()
                else:
                    self.flip_horizontal()
                tiles[self.match[LEFT]].flip_chain(tiles, {self.id}, horiz=True)
            elif self.match[RIGHT]:
                if self.match[LEFT] or self.match[TOP] or self.match[BOTTOM]:
                    return
                self.fixed = False
                self.i += 1
                if self.i % 2 == 1:
                    self.flip_vertical()
                else:
                    self.flip_horizontal()
                tiles[self.match[RIGHT]].flip_chain(tiles, {self.id}, horiz=True)
            elif self.match[TOP]:
                if self.match[BOTTOM] or self.match[LEFT] or self.match[RIGHT]:
                    return
                self.fixed = False
                self.i += 1
                if self.i % 2 == 1:
                    self.flip_horizontal()
                else:
                    self.flip_vertical()
                tiles[self.match[TOP]].flip_chain(tiles, {self.id}, horiz=False)
            elif self.match[BOTTOM]:
                if self.match[TOP] or self.match[LEFT] or self.match[RIGHT]:
                    return
                self.fixed = False
                self.i += 1
                if self.i % 2 == 1:
                    self.flip_horizontal()
                else:
                    self.flip_vertical()
                tiles[self.match[BOTTOM]].flip_chain(tiles, {self.id}, horiz=False)

    def flip_horizontal(self):
        if self.fixed:
            return
        data = []
        for y in self.grid:
            row = []
            for x in y:
                row.insert(0,x)
            data.append(row)
        self.grid = data

    def flip_vertical(self):
        if self.fixed:
            return

        data = []
        for y in self.grid:
            data.insert(0,y)
        self.grid = data

    def rot(self):
        if self.rotation_locked:
            return

        self.grid = list(zip(*self.grid[::-1]))
        # data = copy.deepcopy(self.grid)

        # for y in range(len(self.grid)):
        #     for x in range(len(self.grid[y])):
        #         data[y][x] = self.grid[x][-y]
        # self.grid = data

    def match_right(self, tile):
        match = True
        for y in range(len(self.grid)):
            if self.grid[y][-1] != tile.grid[y][0]:
                match = False
                break
        if match:            
            self.match[RIGHT] = tile.id
            self.rotation_locked = True
        return match

    def match_left(self, tile):
        match = True
        for y in range(len(self.grid)):
            if self.grid[y][0] != tile.grid[y][-1]:
                match = False
                break
        if match:
            self.match[LEFT] = tile.id
            self.rotation_locked = True
        return match

    def match_top(self, tile):
        match = True
        for x in range(len(self.grid[0])):
            if self.grid[0][x] != tile.grid[-1][x]:
                match = False
                break
        if match:
            self.match[TOP] = tile.id
            self.rotation_locked = True
        return match

    def match_bottom(self, tile):
        match = True
        for x in range(len(self.grid[0])):
            if self.grid[-1][x] != tile.grid[0][x]:
                match = False
                break

        if match:
            self.match[BOTTOM] = tile.id
            self.rotation_locked = True
        return match

    def print(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                print(self.grid[y][x], end="")
            print()

    def manipulate(self):
        if self.fixed:
            return

        if self.manip == 0:
            self.manip = 1
        elif self.manip == 1:
            self.rot()
            self.manip = 2
        elif self.manip == 2:
            self.rot()
            self.manip = 3
        elif self.manip == 3:
            self.rot()
            self.manip = 4
        elif self.manip == 4:
            self.rot()
            self.manip = 5
        elif self.manip == 5:
            self.flip_horizontal()
            self.manip = 6
        elif self.manip == 6:
            self.rot()
            self.manip = 7
        elif self.manip == 7:
            self.rot()
            self.manip = 8
        elif self.manip == 8:
            self.rot()
            self.manip = 9
        elif self.manip == 9:
            self.rot()
            self.manip = 10
        elif self.manip == 10:
            self.flip_vertical()
            self.manip = 11
        elif self.manip == 11:
            self.rot()
            self.manip = 12
        elif self.manip == 12:
            self.rot()
            self.manip = 13
        elif self.manip == 13:
            self.rot()
            self.manip = 14
        elif self.manip == 14:
            self.rot()
            self.manip = 15          

with open("test.txt") as file:
#with open("day20.txt") as file:
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
        id, t, b, l, r = tiles[tile].print_edges()
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
        id, t, b, l, r = tiles[tile].print_edges()
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

    def find_tile_with_edges(tiles, ids, dir):
        for t in tiles:
            other_ids = tiles[t].edge_number(dir)
            if ids[0] in other_ids or ids[1] in other_ids:
                return tiles[t]
        assert "Not Found"
    image = []
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
            #orient_piece(start)??
            edge_id = tiles[current.id].edge_number(direction)
            next_tile_id = nodes[edge_id][0] if nodes[edge_id][0] != current.id else nodes[edge_id][1]
            next_tile = tiles[next_tile_id]
            # todo: orient tile
            next_tile.orient(edge_id, LEFT if direction == RIGHT else RIGHT)

            print(" " + str(next_tile.id) +" ", end="")
            #write_image(piece, image)


            current = next_tile
            pieces += 1
        print()
        ids.append(current.id)
        write_image(image, tiles, ids)
        y += 1
        # if direction == BOTTOM and pieces :
        #     direction = RIGHT
        # elif pieces % (width - 1)== 0:
        #     print()
        #     current = upper_left
        #     direction = BOTTOM
        # else:
        # #     start = get_next_piece(start, direction)
        #     pass
        
    image = flip(image, horiztonal=False)
    # TODO multiplier
    im = Image.new(mode="RGB", size = (len(image[0]), len(image)))
    pix = im.load()
    for y in range(len(image)):
        for x in range(len(image[0])):
            print(image[y][x], end="")
            pix[x,y] = (255,0,0) if image[y][x] == "#" else (0,0,0)
        print()
    im.show()

    # find seamonsters
    #if none found, flip horiz

    # scan for seamonster
    #            1111111111
    #   01234567890123456789
    #  0                  # 
    #  1#    ##    ##    ###
    #  2 #  #  #  #  #  #   
    seamonster_offset = [(19,0), (0,1), (5,1), (6,1), (11,1), (12,1), (17,1), (18,1), (19,1), (1,2), (4,2), (7,2), (10,2), (13,2), (16,2)]
    seamonsters_found = 0
    op = [rotate, rotate, rotate, rotate, flip, rotate, rotate, rotate, rotate, lambda x: flip(x,horiztonal=False), rotate, rotate, rotate, rotate ]
    op_index = 0
    while seamonsters_found == 0:
        for y in range(len(image) - 3):
            for x in range(len(image[0]) - 19):
                is_sea_monster = False
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
        
        image = op[op_index](image)
        op_index+=1

    count = 0
    for y in range(len(image)):
        for x in range(len(image[0])):
            if image[y][x] == "#":
                count += 1
    print ("part 2", count)

    def test_match(tiles, i, j):
        t1 = tiles[i]
        t2 = tiles[j]

        matches = None
        if t1.match_right(t2):
            matches = RIGHT
        if t1.match_bottom(t2):
            matches = BOTTOM
        if t1.match_left(t2):
            matches = LEFT
        if t1.match_top(t2):
            matches = TOP

        return matches

# find upper left
    # ops
    # plain
    # flip_h
    # flip_v

    count_fixed = 0
    while count_fixed < len(tiles):
        count_fixed = 0
        for i in range(len(tiles)):
            if tiles[i].fixed:
                count_fixed += 1
            tiles[i].manipulate()
            for j in range(len(tiles)):
                if i == j:
                    continue
                # if tiles[i].fixed and tiles[j].fixed:
                #     continue                
                if test_match(tiles, i, j):
                    print('candidates', i, j, test_match(tiles, i, j), tiles[i].id)
                    tiles[i].fixed = True
                    tiles[j].fixed = True
            
        print(count_fixed)

    c1 = list(filter(lambda t: t.match[TOP] == 0 and t.match[LEFT] == 0 and t.match[RIGHT] != 0 and t.match[BOTTOM] !=0, tiles))
    c2 = list(filter(lambda t: t.match[TOP] == 0 and t.match[RIGHT] == 0 and t.match[LEFT] != 0 and t.match[BOTTOM] !=0, tiles))
    c3 = list(filter(lambda t: t.match[BOTTOM] == 0 and t.match[LEFT] == 0 and t.match[RIGHT] != 0 and t.match[TOP] !=0, tiles))
    c4 = list(filter(lambda t: t.match[BOTTOM] == 0 and t.match[RIGHT] == 0 and t.match[LEFT] != 0 and t.match[TOP] !=0, tiles))

#     # PRINT GRID
    tile_map = {t.id: t for t in tiles}
#     assert c1
#     printed = set()
#     t = c1[0]
# #    while len(printed) < len(tiles):
#     printed.add(t.id)
#     print(t.id, "-", end="")
#     while t.match[RIGHT]:
#         t = tile_map[t.match[RIGHT]]
#         printed.add(t.id)
#         print(t.id, "-", end="")
#     print()

#     exit(-1)

    # We've matched rotations
    # now we need to try flipping

    while not c1 or not c2 or not c3 or not c4:
        for i in range(len(tiles)):
            tiles[i].flip_horizontal()
            for j in range(len(tiles)):
                if i == j:
                    continue
                if test_match(tiles, i, j):
                    print("matched", i, j, tiles[i].id, tiles[j].id)
                    exit(-1)

        c1 = list(filter(lambda t: t.match[TOP] == 0 and t.match[LEFT] == 0 and t.match[RIGHT] != 0 and t.match[BOTTOM] !=0, tiles))
        c2 = list(filter(lambda t: t.match[TOP] == 0 and t.match[RIGHT] == 0 and t.match[LEFT] != 0 and t.match[BOTTOM] !=0, tiles))
        c3 = list(filter(lambda t: t.match[BOTTOM] == 0 and t.match[LEFT] == 0 and t.match[RIGHT] != 0 and t.match[TOP] !=0, tiles))
        c4 = list(filter(lambda t: t.match[BOTTOM] == 0 and t.match[RIGHT] == 0 and t.match[LEFT] != 0 and t.match[TOP] !=0, tiles))

    c1 = c1[0] if c1 else Tile(-1,[])
    c2 = c2[0] if c2 else Tile(-1,[])
    c3 = c3[0] if c3 else Tile(-1,[])
    c4 = c4[0] if c4 else Tile(-1,[])
    print(c1.id, c2.id)
    print(c3.id, c4.id)
    print(c1.id * c2.id * c3.id * c4.id)