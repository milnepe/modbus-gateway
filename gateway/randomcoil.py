import random


def gen_coillist(max_coils: int) -> list:
    """Generate a random list of coils for testing"""
    randomlist = []
    for _ in range(0, random.randint(1, max_coils)):
        coil = random.randint(0, max_coils - 1)
        while coil in randomlist:
            coil = random.randint(0, max_coils - 1)
        randomlist.append(coil)
    return randomlist


if __name__ == "__main__":
    print(gen_coillist(max_coils=4))
