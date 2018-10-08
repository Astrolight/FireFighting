from World import World

test_world = World(1000, 1)

for _ in range(1000):
    test_world.step()