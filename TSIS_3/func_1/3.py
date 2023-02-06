def solve(numheads, numlegs):
    chickens = 0
    rabbits = 0
    chickens = (4*numheads - numlegs)/2
    rabbits = numheads - chickens
    return {"chickens": chickens, "rabbits": rabbits}

print(solve(35, 92))