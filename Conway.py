import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

universe = np.zeros((6, 6))

beacon = [[1, 1, 0, 0],
          [1, 1, 0, 0],
          [0, 0, 1, 1],
          [0, 0, 1, 1]]

universe[1:5, 1:5] = beacon

plt.figure()
plt.imshow(universe, cmap='binary')
plt.show()

new_universe = np.copy(universe)


def survival(x, y):
    """
    :param x: x coordinate of the cell
    :param y: y coordinate of the cell
    """
    # Find the number of living neighbours by taking the sum of the 8 surrounding grid squares
    num_neighbours = np.sum(universe[x-1:x+2, y-1:y+2]) - universe[x, y]

    # Apply the rules of Life
    if universe[x, y] and not 2 <= num_neighbours <= 3:
        new_universe[x, y] = 0
    elif num_neighbours == 3:
        new_universe[x, y] = 1


def generation():
    global universe
    for i in range(universe.shape[0]):
        for j in range(universe.shape[1]):
            survival(i, j)
    universe = np.copy(new_universe)


# # Animation
fig = plt.figure()
plt.axis('off')
ims = []
for i in range(30):
    ims.append((plt.imshow(universe, cmap='Purples'),))
    generation()
im_ani = animation.ArtistAnimation(fig, ims, interval=700, repeat_delay=1000,
                                   blit=True)

mywriter = animation.FFMpegWriter()
im_ani.save('beacon.mp4', writer=mywriter)




#
universe = np.zeros((100, 100))


# beacon = [[0, 0, 1, 1],
#           [0, 0, 1, 1],
#           [1, 1, 0, 0],
#           [1, 1, 0, 0]]

# universe[1:3, 1:3], universe[3:5, 3:5] = 1, 1

# penta oscillator
k = len(universe) // 2 - 1
# universe[k-1:k+2, k-3:k+5] = 1
# universe[k, k-2], universe[k, k+3] = 0, 0

# spread thingy
universe[k:k+3, k:k+3] = 1
universe[k,k], universe[k+2, k], universe[k+1:k+3, k+2] = 0, 0, 0

new_universe = np.copy(universe)

# plt.figure('before')
# plt.imshow(universe, cmap='binary')
# plt.show()


def survival(x, y):
    """
    # :param x: x coordinate
    # :param y: y coordinate
    # :return: coordinates of surroundings
    """
    num_neighbours = np.sum(universe[x-1:x+2, y-1:y+2]) - universe[x, y]
    if universe[x, y] == 1:
        if num_neighbours < 2 or num_neighbours > 3:
            new_universe[x, y] = 0
    elif universe[x, y] == 0:
        if num_neighbours == 3:
            new_universe[x, y] = 1


def generation():
    for i in range(len(new_universe)):
        for j in range(len(new_universe)):
            survival(i, j)
    global universe; universe = np.copy(new_universe)

# generation()
# plt.figure('aft')
# plt.imshow(universe, cmap='binary')
# plt.show()

# # Animation
fig1 = plt.figure()
plt.axis('off')

ims = []
for i in range(1105):
    ims.append((plt.imshow(universe, cmap='Purples'),))
    generation()

im_ani = animation.ArtistAnimation(fig1, ims, interval=10, repeat_delay=3000,
                                   blit=True)

# mywriter = animation.FFMpegWriter()
# im_ani.save('rpentomino.mp4', writer=mywriter)

