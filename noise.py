"""
What is this?
This is a Perlin-Noise-Generator which can generate Perlin-Noise.

How do I use it?
You can run following script:

>>> from PerlinNoise import Perlin

>>> seed = "My Beautiful Seed :)"
>>> # the seed is optional and has only be set if you want to have the same result

>>> width, height = 512, 256
>>> # the size is optional but it's recommended to insert the values you need

>>> octave = 10
>>> # the octave is optional but note that a higher value results in a smoother Noise and needs more time to process

>>> my_perlin_generator = Perlin(
>>>     seed=seed,
>>>     width=width,
>>>     height=height,
>>>     octave=octave
>>> )

>>> # call the generator by `Perlin.generate()` or directly
>>> my_perlin_result = my_perlin_generator()
>>> # your perlin-noise is now in a 2D-list with floats between 0 and 1


If you want to see the result here is a quick example:

>>> from matplotlib import pyplot as plt

>>> plt.figure(dpi=100)
>>> plt.imshow(my_perlin_result, cmap="gray")
>>> # other cmap's I recommend to try are "gist_earth", "plasma" and "hot"
>>> plt.show()

Did you implement it your own?
No, I found an example written in `C#` and I rewrote it in Python 3.
If you want you can check the original code here: https://devmag.org.za/2009/04/25/perlin-noise/ out.

"""

from random import Random
from typing import Union, Optional, Callable

__all__ = ("Perlin",)
float2d = list[list[float]]


class Perlin:
    """The class for PerlinNoise."""

    def __init__(
        self,
        *,
        seed: Optional[Union[str, bytes, bytearray, int, float]] = None,
        width: int = 128,
        height: int = 128,
        octave: int = 1,
    ):
        """
        Parameters
        ----------
        seed: :class:`str`, :class:`bytes`, class:`bytearray`, :class:`int`, :class:`float`, optional
            The seed for random generator.
        width, height: :class:`int`
            The size of the list for the noise.
        octave: :class:`int`
            The octave for the noise generation.
        """
        self.random: Random = Random(seed)
        self.size = (width, height)
        self._octave = octave

    @property
    def width(self) -> int:
        """
        Returns
        -------
        :class:`int`
            The width of the Perlin-Noise-List
        """
        return self.size[0]

    @property
    def height(self) -> int:
        """
        Returns
        -------
        :class:`int`
            The height of the Perlin-Noise-List
        """
        return self.size[1]

    @property
    def octave(self) -> int:
        """
        Returns
        -------
        :class:`int`
            The octave of the Perlin-Noise
        """
        return self._octave

    def generate(self) -> float2d:
        """
        Generates the Perlin Noise.

        Returns
        -------
        :class:`list[list[float]]`
            The generated Perlin Noise.
        """
        return self._generate_perlin_noise(self._generate_white_noise())

    __call__ = generate

    @staticmethod
    def interpolate(x: float, y: float, /, alpha: float) -> float:
        """
        Interpolates two values in dependency to :arg:`alpha`.

        Parameters
        ----------
        x, y: :class:`float`
            The values to interpolate linearly.
        alpha: :class:`float`
            The value from which the interpolation depends.

        Returns
        -------
        :class:`float`
            The result from the interpolation.
        """
        return x * (1 - alpha) + alpha * y

    def _generate_white_noise(self) -> float2d:
        """
        Generates a blank/white noise with complete random values
        with no relationship.

        Returns
        -------
        :class:`list[list[float]]`
            The new generated "white noise"
        """
        width: int = self.size[0]
        height: int = self.size[1]
        random: Random = self.random
        noise: float2d = []

        for h in range(height):
            row: list[float] = []
            for w in range(width):
                row.append(random.random() % 1)
            noise.append(row)

        return noise

    def _generate_smooth_noise(
        self, base: float2d, octave: Optional[int] = None
    ) -> float2d:
        """
        Generates a smoothed noise from a blank/white noise.

        Notes
        -----
        The sizes given into the constructor are ignored and the sizes from
        the :arg:`base` are used.

        Parameters
        ----------
        base: :class:`list[list[float]]`
            It's recommended to input directly the output from
            :meth:`Perlin._generate_white_noise`.
        octave: :class:`int`, optional
            The customisable octave
            (needed for the generation of the perlin noise).

        Returns
        -------
        :class:`list[list[float]]`
            The new "smoothed noise".
        """
        interpolate: Callable[[float, float, float], float] = self.interpolate

        noise: float2d = []

        height: int = len(base)
        width: int = len(base[0])

        sample_period: int = 1 << (octave or self.octave)
        sample_frequency: float = 1 / sample_period

        for h in range(height):
            sample_h0: int = int(int(h / sample_period) * sample_period)
            sample_h1: int = int(int(sample_h0 + sample_period) % height)
            vertical_blend: float = (h - sample_h0) * sample_frequency

            row: list[float] = []
            for w in range(width):
                sample_w0: int = int(int(w / sample_period) * sample_period)
                sample_w1: int = int(int(sample_w0 + sample_period) % width)
                horizontal_blend: float = (w - sample_w0) * sample_frequency

                top: float = interpolate(
                    base[sample_h0][sample_w0],
                    base[sample_h1][sample_w0],
                    horizontal_blend,
                )
                bottom: float = interpolate(
                    base[sample_h1][sample_w1],
                    base[sample_h0][sample_w1],
                    horizontal_blend,
                )

                row.append(interpolate(top, bottom, vertical_blend))
            noise.append(row)

        return noise

    def _generate_perlin_noise(self, base: float2d) -> float2d:
        """
        Generates a perlin noise from a smoothed noise.

        Notes
        -----
        The sizes given into the constructor are ignored and the sizes from
        the :arg:`base` are used.

        Parameters
        ----------
        base: :class:`list[list[float]]`
            It's recommended to input directly the output from
            :meth:`Perlin._generate_white_noise`.

        Returns
        -------
        :class:`list[list[float]]`
            The new Perlin Noise.
        """
        height: int = len(base)
        width: int = len(base[0])

        octave: int = self.octave

        persistence: float = 0.5
        amplitude: float = 1.0
        total_amplitude: float = 0.0

        smooth: list[float2d] = []
        noise: float2d = [[0.0 for _ in range(width)] for _ in range(height)]

        # generate smooth noise
        for o in range(octave):
            smooth.append(self._generate_smooth_noise(base, o))

        # blend noise together
        # for o in range(octave-1, -1, -1):  # <- original in code
        for o in range(octave):  # <- worked for me
            amplitude *= persistence
            total_amplitude += amplitude

            for h in range(height):
                for w in range(width):
                    noise[h][w] += smooth[o][h][w] * amplitude

        # normalisation
        for h in range(height):
            for w in range(width):
                noise[h][w] /= total_amplitude

        return noise


if __name__ == "__main__":
    from matplotlib import pyplot as plt

    square_size: int = 1 << 9
    perlin: Perlin = Perlin(
        seed="#AU", octave=20, width=square_size, height=square_size
    )
    perlin_map: float2d = perlin()

    plt.figure(dpi=square_size)
    plt.imshow(
        perlin_map,
        # cmap="gist_earth")
        # cmap="gray")
        # cmap="plasma")
        cmap="hot",
    )
    plt.show()
