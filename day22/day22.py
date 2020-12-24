
decks = {}
player = -1
#with open("infinite.txt") as file:
#with open("test.txt") as file:
with open("day22.txt") as file:
    for line in file.read().splitlines():
        if not line:
            continue
        elif "Player" in line:
            player += 1
            decks[player] = []
        else:
            decks[player].append(int(line))

# print(decks)

def play_combat(decks):    
    while decks[0] and decks[1]:
        p1 = decks[0].pop(0)
        p2 = decks[1].pop(0)
        # print ("Player 1: plays:", p1)
        # print ("Player 2: plays:", p2)
        if p1 > p2:
            # print ("Player 1 wins the round!")
            decks[0].append(p1)
            decks[0].append(p2)
        else:
            assert p1 != p2
            # print ("Player 2 wins the round!")
            decks[1].append(p2)
            decks[1].append(p1)

def score(decks):
    winner = decks[0] if len(decks[1]) == 0 else decks[1]
    score = 0
    val = len(winner)
    while val > 0:
        # print (winner[-val],"*",val)
        score += val * winner[-val]
        val -= 1
    return score

part1_decks = { 0: decks[0].copy(), 1: decks[1].copy() }
#play_combat(part1_decks)
## print ("Part 1", score(part1_decks))

def play_recursive_combat(decks, game):
    print ("=== Game",game,"===")
    # print()
    round = 1
    previous_rounds={}
    recursion_forfeit = False
    # TODO recursion check
    while decks[0] and decks[1] and not recursion_forfeit:
        print ("-- Round", round, "(Game", game,")--")
        # print ("Player 1's deck:", decks[0])
        # print ("Player 2's deck:", decks[1])

        key = (",".join([str(d) for d in decks[0]]), ",".join([str(d) for d in decks[1]]))
        if key in previous_rounds:
            recursion_forfeit = True
            break
        else:
            previous_rounds[key] = True

        assert len(decks[0]) > 0
        assert len(decks[1]) > 0
        p1 = decks[0].pop(0)
        p2 = decks[1].pop(0)

        # print ("Player 1: plays:", p1)
        # print ("Player 2: plays:", p2)
        if len(decks[0]) >= p1 and len(decks[1]) >= p2:
            # print ("Playing a sub-game to determine the winner..")
            winner = play_recursive_combat({ 0: decks[0].copy()[:p1], 1: decks[1].copy()[:p2] }, game+1)
            if winner == 1:
                # print ("The winner of game", game, "is player 1!")
                decks[0].append(p1)
                decks[0].append(p2)
            else:
                assert winner == 2
                # print ("The winner of game", game, "is player 2!")
                decks[1].append(p2)
                decks[1].append(p1)
            # print()
        else:
            if p1 > p2 :
                # print ("Player 1 wins round", round, "of game", game, "!")
                decks[0].append(p1)
                decks[0].append(p2)
            else:
                assert p1 != p2
                # print ("Player 2 wins round", round, "of game", game, "!")
                decks[1].append(p2)
                decks[1].append(p1)
            # print()
        
        round += 1
    # If recursion ends, 
    if recursion_forfeit:
        return 1
    return 2 if len(decks[0]) == 0 else 1

play_recursive_combat(decks, 1)
print ("Part 2", score(decks))
