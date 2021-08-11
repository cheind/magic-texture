import numpy as np
import pandas as pd
import time
import magictex as mtex


def main():
    N = 10
    sizes = 2 ** np.arange(8, 12)

    for s in sizes:
        coords = mtex.coordinate_grid((s, s))
        t = time.time()
        for _ in range(N):
            coords = mtex.coordinate_grid((s, s))
        t_coords = (time.time() - t) / N

        t = time.time()
        for _ in range(N):
            _ = mtex.magic(coords, depth=3)
        t_magic = (time.time() - t) / N
        print(
            f"{(s, s)}: coords {t_coords:.3f} sec/image, magic {t_magic:.3f} sec/image"
        )


if __name__ == "__main__":
    main()
