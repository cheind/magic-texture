import matplotlib.pyplot as plt

import magictex as mtex


def main():
    coords = mtex.coordinate_grid((1024, 1024))
    tex1 = mtex.magic(coords, scale=2.5, depth=3, distortion=3.0)
    tex2 = mtex.magic(coords, scale=0.8, depth=5, distortion=2.0)

    fig, axs = plt.subplots(1, 2, sharex=True, sharey=True)
    axs[0].imshow(tex1)
    axs[1].imshow(tex2)
    plt.show()


if __name__ == "__main__":
    main()