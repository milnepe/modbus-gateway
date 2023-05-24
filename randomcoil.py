import random

def gen_coillist(max_coils: int) -> list:
    """Generate a random list of coils for testing"""
    randomlist = []
    for i in range(0,random.randint(1, max_coils)):
        n = random.randint(0, max_coils - 1)
        while n in randomlist:
            n = random.randint(0, max_coils - 1)    
        randomlist.append(n)
    return randomlist

print(gen_coillist(max_coils=4))