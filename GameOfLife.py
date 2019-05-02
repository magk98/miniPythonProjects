import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

ON = 255
OFF = 0
vals = [ON, OFF]


def random_grid(N):
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)


def add_pattern(i, j, grid, pattern):
    if pattern == 'glider':
        add_glider(i, j, grid)
    elif pattern == 'block':
        add_block(i, j, grid)
    elif pattern == 'loaf':
        add_loaf(i, j, grid)
    elif pattern == 'diehard':
        add_diehard(i, j, grid)
    elif pattern == 'gosper_glider_gun':
        add_gosper_glider_gun(i, j, grid)


def add_diehard(i, j, grid):
    diehard = np.array([[OFF, OFF, OFF, OFF, OFF, OFF, ON, OFF],
                        [ON, ON, OFF, OFF, OFF, OFF, OFF, OFF],
                        [OFF, ON, OFF, OFF, OFF, ON, ON, ON]])
    grid[i:i+3, j:j+8] = diehard


def add_gosper_glider_gun(i, j, grid):
    gun = np.array([    [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
                        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON,  OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
                        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON,  OFF, ON,  OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
                        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON,  ON,  OFF, OFF, OFF, OFF, OFF, OFF, ON,  ON,  OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON,  ON, OFF],
                        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON,  OFF, OFF, OFF, ON,  OFF, OFF, OFF, OFF, ON,  ON,  OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON,  ON, OFF],
                        [OFF, ON, ON,   OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON,  OFF, OFF, OFF, OFF, OFF, ON,  OFF, OFF, OFF, ON,  ON,  OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
                        [OFF, ON, ON,   OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON,  OFF, OFF, OFF, ON,  OFF, ON,  ON,  OFF, OFF, OFF, OFF, ON,  OFF, ON,  OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
                        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON,  OFF, OFF, OFF, OFF, OFF, ON,  OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON,  OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
                        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON,  OFF, OFF, OFF, ON,  OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
                        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, ON,  ON,  OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF],
                        [OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF]])
    grid[i:i+11, j:j+38] = gun


def add_loaf(i, j, grid):
    loaf = np.array([[OFF, ON, ON, OFF],
                     [ON, OFF, OFF, ON],
                     [OFF, ON, OFF, ON],
                     [OFF, OFF, ON, OFF]])
    grid[i:i+4, j:j+4] = loaf


def add_block(i, j, grid):
    block = np.array([[OFF, ON],
                      [ON, ON]])
    grid[i:i+2, j:j+2] = block


def add_glider(i, j, grid):
    glider = np.array([[OFF, OFF, ON],
                       [ON, OFF, ON],
                       [OFF, ON, ON]])
    grid[i:i+3, j:j+3] = glider


def update(frameNum, img, grid, N):
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
            if grid[i, j] == ON:
                if total < 2 or total > 3:
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img


def main():
    parser = argparse.ArgumentParser(description="Game of life")
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='mov_file', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--pattern', dest='pattern', required=False)
    args = parser.parse_args()

    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    grid = np.array([])
    if args.pattern:
        grid = np.zeros(N*N).reshape(N, N)
        add_pattern(1, 1, grid, args.pattern)
    else:
        grid = random_grid(N)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                  frames=10, interval=updateInterval, save_count=50)
    if args.mov_file:
        ani.save(args.mov_file, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


if __name__ == '__main__':
    main()
