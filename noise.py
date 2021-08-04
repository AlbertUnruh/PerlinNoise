"""
MIT License

Copyright (c) 2021 AlbertUnruh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

----------

Implementation followed by http://devmag.org.za/2009/04/25/perlin-noise/.
"""


from random import Random

__all__ = (
    "Perlin",
)


class Perlin:
    """The class for PerlinNoise."""

    def __init__(self, *, seed=None, width=128, height=128, octave=1):
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
        self.random = Random(seed)
        self.size = (width, height)
        self._octave = octave

    @property
    def width(self):
        """
        Returns
        -------
        :class:`int`
            The width of the Perlin-Noise-List
        """
        return self.size[0]

    @property
    def height(self):
        """
        Returns
        -------
        :class:`int`
            The height of the Perlin-Noise-List
        """
        return self.size[1]

    @property
    def octave(self):
        """
        Returns
        -------
        :class:`int`
            The octave of the Perlin-Noise
        """
        return self._octave

    def generate(self):
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
    def interpolate(x, y, /, alpha):
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

    def _generate_white_noise(self):
        """
        Generates a blank/white noise with complete random values
        with no relationship.

        Returns
        -------
        :class:`list[list[float]]`
            The new generated "white noise"
        """
        width, height = self.size  # type: int
        random = self.random  # type: Random
        noise = []  # type: list[list[float]]

        for h in range(height):
            row = []
            for w in range(width):
                row.append(random.random() % 1)
            noise.append(row)

        return noise

    def _generate_smooth_noise(self, base, octave=None):
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
        interpolate = self.interpolate

        noise = []  # type: list[list[float]]

        height = len(base)  # type: int
        width = len(base[0])  # type: int

        sample_period = 1 << (octave or self.octave)  # type: int
        sample_frequency = 1 / sample_period  # type: float

        for h in range(height):
            sample_h0 = int(int(h / sample_period) * sample_period)
            sample_h1 = int(int(sample_h0 + sample_period) % height)
            vertical_blend = (h - sample_h0) * sample_frequency

            row = []
            for w in range(width):
                sample_w0 = int(int(w / sample_period) * sample_period)
                sample_w1 = int(int(sample_w0 + sample_period) % width)
                horizontal_blend = (w - sample_w0) * sample_frequency

                top = interpolate(base[sample_h0][sample_w0],
                                  base[sample_h1][sample_w0],
                                  horizontal_blend)
                bottom = interpolate(base[sample_h1][sample_w1],
                                     base[sample_h0][sample_w1],
                                     horizontal_blend)

                row.append(interpolate(top, bottom, vertical_blend))
            noise.append(row)

        return noise

    def _generate_perlin_noise(self, base):
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
        height = len(base)  # type: int
        width = len(base[0])  # type: int

        octave = self.octave  # type: int

        persistence, amplitude, total_amplitude = .5, 1., 0

        smooth = []  # type: list[list[list[float]]]
        noise = [[0. for _ in range(width)] for _ in range(height)]  # type: list[list[float]]

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


if __name__ == '__main__':
    from matplotlib import pyplot as plt

    square_size = 1 << 9
    perlin = Perlin(seed="#AU", octave=20,
                    width=square_size, height=square_size)
    perlin_map = perlin()

    plt.figure(dpi=square_size)
    plt.imshow(perlin_map,
               # cmap="gist_earth")
               # cmap="gray")
               # cmap="plasma")
               cmap="hot")
