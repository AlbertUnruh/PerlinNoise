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

from noise import *

__all__ = (Perlin,)

__author__ = "AlbertUnruh"
__copyright__ = "Copyright (c) 2021 AlbertUnruh"
__credits__ = ["AlbertUnruh", "Staubfinger"]

__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "AlbertUnruh"
__email__ = None
__status__ = "Production"
