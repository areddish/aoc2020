def play_game(turns, start, nodes, max_cup_label):
    current_cup = start_label
    move = 0
    while move < turns:
        # Snip out a sub graph of length 3
        sub_graph_start = nodes[current_cup]
        pickup = []
        cur = sub_graph_start
        for _ in range(3):
            pickup.append(cur)
            cur = nodes[cur]

        # Find the next destination cup
        dest_cup = current_cup - 1
        while dest_cup in pickup or dest_cup < 1:
            dest_cup -= 1
            if dest_cup < 1:
                dest_cup = max_cup_label

        # remove subgraph, by updating nodes
        nodes[current_cup] = cur

        # Put back in after dest_cup
        temp = nodes[dest_cup]
        nodes[dest_cup] = sub_graph_start
        nodes[nodes[nodes[sub_graph_start]]] = temp

        # Move onto the next cup
        current_cup = cur
        move += 1


#### PART 1

day23_input = [int(x) for x in "389125467"]
#day23_input = [int(x) for x in "562893147"]

start_label = day23_input[0]

# Create the mapping node -> node
nodes = {day23_input[0]: day23_input[1]}
for x in range(1, len(day23_input)-1):
    nodes[day23_input[x]] = day23_input[x+1]
# Create the cycle
nodes[day23_input[-1]] = day23_input[0]

play_game(100, start_label, nodes, max(day23_input))

# Solution
start = nodes[1]
nums = []
for _ in range(len(day23_input)-1):
    nums.append(str(start))
    start = nodes[start]
print("part 1", "".join(nums))

#### PART 2

#day23_input = [int(x) for x in "389125467"]
day23_input = [int(x) for x in "562893147"]
max_cup_label = max(day23_input)
start_label = day23_input[0]
nodes = { day23_input[0]: day23_input[1]}
for x in range(1, len(day23_input)-1):
    nodes[day23_input[x]] = day23_input[x+1]
for i in range(max_cup_label+1,1000000+1):
    nodes[i] = i+1

# connect the two graphs
nodes[day23_input[-1]] = max_cup_label+1
# make it cyclical
nodes[1000000] = start_label

play_game(10000000, start_label, nodes, 1000000)

# Part 2
print("part 2", nodes[1] * nodes[nodes[1]])