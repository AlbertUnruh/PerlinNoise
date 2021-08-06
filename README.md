# Perlin Noise
###### Implementation in Python3 by [AlbertUnruh](https://github.com/AlbertUnruh).

---

### What is this?
This is a Perlin-Noise-Generator which can generate Perlin-Noise.

### How do I use it?
You can run following script:
```python
from PerlinNoise import Perlin

seed = "My Beautiful Seed :)"
# the seed is optional and has only be set if you want to have the same result

width, height = 512, 256
# the size is optional but it's recommended to insert the values you need

octave = 10
# the octave is optional but note that a higher value results in a smoother Noise and needs more time to process

my_perlin_generator = Perlin(
    seed=seed,
    width=width,
    height=height,
    octave=octave
)

# call the generator by `Perlin.generate()` or directly
my_perlin_result = my_perlin_generator()
# your perlin-noise is now in a 2D-list with floats between 0 and 1
```

If you want to see the result here is a quick example:
```python
from matplotlib import pyplot as plt

plt.figure(dpi=100)
plt.imshow(my_perlin_result, cmap="gray")
# other cmap's I recommend to try are "gist_earth", "plasma" and "hot"
plt.show()
```

### Did you implement it your own?
No, I found an example written in `C#` and I rewrote it in `Python 3`.
If you want you can check the original code [here](http://devmag.org.za/2009/04/25/perlin-noise/) out.


## Examples
*The examples had following values in the constructor:*
 - `seed="#AU"`
 - `widht=512`
 - `height=512`
 - `octave=20`

`cmap = "gray"`
![Perlin Noise with cmap gray](/images/size512octave20colorgray.png)

`cmap = "gist_earth"`
![Perlin Noise with cmap gist_earth](/images/size512octave20colorgist_earth.png)

`cmap = "hot"`
![Perlin Noise with cmap hot](/images/size512octave20colorhot.png)

`cmap = "plasma"`
![Perlin Noise with cmap plasma](/images/size512octave20colorplasma.png)
