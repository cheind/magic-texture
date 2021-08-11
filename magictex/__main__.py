import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid

import magictex as mtex


def main():
    rng = np.random.default_rng(seed=1234)
    fig = plt.figure(figsize=(12, 9))
    grid = ImageGrid(fig, 111, nrows_ncols=(3, 4), axes_pad=0.1)

    # Create canonical coordinates for 1024x1024 image
    coords = mtex.coordinate_grid((1024, 1024))
    for ax in grid:
        # Transform coordinates, distort and generate texture
        tex = mtex.magic(
            mtex.random_transform(coords, rng),
            depth=rng.integers(1, 5),
            distortion=rng.uniform(2, 3),
            rng=rng,
        )
        # Plot
        ax.get_yaxis().set_ticks([])
        ax.get_xaxis().set_ticks([])
        ax.imshow(tex)
    plt.show()


if __name__ == "__main__":
    main()
