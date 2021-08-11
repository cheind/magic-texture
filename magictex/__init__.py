"""Generates psychedelic color textures in the spirit of Blender's magic texture shader using Python/Numpy

https://github.com/cheind/magic-texture
"""
from typing import Tuple
import numpy as np


def coordinate_grid(shape: Tuple[int, int], dtype=np.float32):
    """Returns a three-dimensional coordinate grid of given shape for use in `magic`."""
    x = np.linspace(-1, 1, shape[1], endpoint=True, dtype=dtype)
    y = np.linspace(-1, 1, shape[0], endpoint=True, dtype=dtype)
    X, Y = np.meshgrid(x, y)
    XYZ = np.stack((X, Y, np.ones_like(X)), -1)
    return XYZ


def magic(
    coords: np.ndarray,
    scale: float = 1.0,
    offset: float = 0.0,
    depth: int = 2,
    distortion: float = 5.0,
    rng: np.random.Generator = None,
):
    """Returns color magic color texture.

    The implementation is based on Blender's (https://www.blender.org/) magic
    texture shader. The following adaptions are made: we exchange the nested
    if-cascade by a probabilistic iterative approach, the geometric coordinates
    are not fixed but an argument to this method.

    Kwargs
    ------
    coords: HxWx3 array
        Coordinates transformed into colors by this method. See
        `magictex.coordinate_grid` to generate the default.
    scale: float
        Scale of the pattern. Scales < 1. lead to enlargement of structures,
        scales > 1 to smaller patterns.
    offset: float
        Translational offset applied to generated pattern.
    depth: int
        Number of transformations applied. Higher numbers lead to more
        nested patterns.
    distortion: float
        Distortion of patterns. Larger values indicate more distortion,
        lower values tend to generate smoother patterns.
    rng: np.random.Generator
        Optional random generator to draw samples from.

    Returns
    -------
    colors: HxWx3 array
        Three channel color image in range [0,1]
    """
    rng = rng or np.random.default_rng()
    H, W = coords.shape[:2]
    XYZ = coords * scale + np.array([offset / W, offset / H, 1.0])
    x = np.sin((XYZ[..., 0] + XYZ[..., 1] + XYZ[..., 2]) * distortion)
    y = np.cos((-XYZ[..., 0] + XYZ[..., 1] - XYZ[..., 2]) * distortion)
    z = -np.cos((-XYZ[..., 0] - XYZ[..., 1] + XYZ[..., 2]) * distortion)

    if depth > 0:
        x *= distortion
        y *= distortion
        z *= distortion
        y = -np.cos(x - y + z)
        y *= distortion

    xyz = [x, y, z]
    fns = [np.cos, np.sin]
    for _ in range(1, depth):
        axis = rng.choice(3)
        fn = fns[rng.choice(2)]
        signs = rng.binomial(n=1, p=0.5, size=4) * 2 - 1

        xyz[axis] = signs[-1] * fn(
            signs[0] * xyz[0] + signs[1] * xyz[1] + signs[2] * xyz[2]
        )
        xyz[axis] *= distortion

    x, y, z = xyz
    x /= 2 * distortion
    y /= 2 * distortion
    z /= 2 * distortion
    c = 0.5 - np.stack((x, y, z), -1)
    np.clip(c, 0, 1.0)
    return c
