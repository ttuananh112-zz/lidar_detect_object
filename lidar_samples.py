import numpy as np
import matplotlib.pyplot as plt


def get_ranges(filename):
    samples = []
    with open(filename) as fp:
        lines = fp.readlines()
        for line in lines:
            parts = line.split(':')
            if parts[0] == 'ranges':
                samples_raw = parts[1]
                # cut [ ]
                samples_raw = samples_raw[1:-2]
                # replace inf to 0
                samples_raw = samples_raw.replace('inf', '0')
                list_samples_str = samples_raw.split(',')[:-1]
                # parse to int list
                list_samples_float = list(map(float, list_samples_str))
                samples.append(list_samples_float)

    return np.array(samples)


def re_arrange(samples):
    x = []
    y = []
    for i, r in enumerate(samples):
        x.append(r*np.sin(2*np.pi*i/len(samples)))
        y.append(r*np.cos(2*np.pi*i/len(samples)))
    return x, y


# click left/right to move to the next sample
def key_event(e):
    global curr_pos
    global plots

    if e.key == "right":
        curr_pos = curr_pos + 1
    elif e.key == "left":
        curr_pos = curr_pos - 1
    else:
        return
    curr_pos = curr_pos % len(plots)

    ax.cla()
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.scatter(plots[curr_pos][0], plots[curr_pos][1], s=5)
    fig.canvas.draw()
    print(curr_pos)


def distance(coord_last, coord_curr):
    x_last, y_last = coord_last
    x_curr, y_curr = coord_curr
    dist = np.sqrt((x_last - x_curr)**2 + (y_last - y_curr)**2)
    return dist

# def find_cluster(plots):
#     for idx, coord in enumerate(plots):
#         if idx > 0:
#             dist = distance(coord_last, coord)
#
#             if coord != (0, 0):
#                 coord_last = coord
#


if __name__ == '__main__':
    curr_pos = 0
    # refine samples
    samples_np = get_ranges('lidar_samples/1-1.txt')
    plots = []
    for idx in range(samples_np.shape[0]):
        x, y = re_arrange(samples_np[idx])
        plots.append((x, y))

    fig = plt.figure()
    fig.canvas.mpl_connect('key_press_event', key_event)
    ax = fig.add_subplot(111)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.scatter(plots[curr_pos][0], plots[curr_pos][1], s=5)
    plt.show()
