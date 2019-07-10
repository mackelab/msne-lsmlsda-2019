from io import BytesIO
from IPython.display import display, Image
from PIL.Image import fromarray
import numpy as np
from ipywidgets import interact
from numba import jit


""" After some tricks:
https://gist.github.com/kylemcdonald/2f1b9a255993bf9b2629
"""


@jit(nopython=True)
def color_pos_neg(a, c_neg, c_mid, c_pos, min_neg, max_pos):
    colored = np.zeros((a.shape[0], a.shape[1], 3), dtype=np.uint8)
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            # TODO find a way to do a fast LAB interpolation
            if a[i, j] > 0:
                val = a[i, j] / max_pos
                colored[i, j] = (val * c_pos + (1 - val) * c_mid).astype(np.uint8)
            else:
                val = a[i, j] / min_neg
                colored[i, j] = (val * c_neg + (1 - val) * c_mid).astype(np.uint8)
    return colored


def overlay_multiple(*stacks, colors=((255, 127, 0), (0, 127, 255))):
    if stacks[0].dtype == np.uint8:
        multiplier = 1 / 255.0
        output_type = np.uint8
    else:
        multiplier = 1
        output_type = stacks[0].dtype
    overlay = np.zeros(stacks[0].shape + (3,), dtype=output_type)
    color_index = (None,) * len(stacks[0].shape) + (slice(None),)

    for stack, color in zip(stacks, colors):
        overlay += (
            stack[..., None] * (np.array(color) * multiplier)[color_index]
        ).astype(output_type)
    return overlay


def array_to_img(
    image, vmax=None, vmin=None, invert=True, mincolor=None, maxcolor=None, retina=True
):

    try:
        if image.dtype == np.bool:
            isbool = True
        else:
            isbool = False
    except AttributeError:
        isbool = False

        if invert:
            image = fromarray(np.logical_not(image).view(dtype=np.uint8), mode="1")
        else:
            image = fromarray(image.view(dtype=np.uint8), mode="1")
    else:
        if vmax is None and vmin is None:
            clipped = False
        else:
            clipped = True

        if vmax is None:
            vmax = np.nanmax(image)

        # check if the image has negative values, if not, use full range
        if vmin is None:
            vmin = np.nanmin(image)

        if clipped:
            image = np.clip(image, vmin, vmax) - vmin

        if vmin >= 0:
            if invert:
                image = vmax - vmin - image

        else:
            try:
                assert len(image.shape) == 2
            except AssertionError:
                raise Exception("Image containing negative values has to be 2D")

            if mincolor is None:
                mincolor = np.array([0, 180, 255])
            if maxcolor is None:
                maxcolor = np.array([255, 10, 0])

            if invert:
                midcolor = np.array([255, 255, 255])
            else:
                midcolor = np.array([0, 0, 0])

            image = color_pos_neg(image, mincolor, midcolor, maxcolor, vmin, vmax)

        if image.ndim == 2:
            image = fromarray(
                (image * (255 / (vmax - vmin))).astype(np.uint8), mode="L"
            )
        else:
            image = fromarray(image, mode="RGB")

    return image


def display_array(ar, browse_axes=None, **kwargs):
    """ Fast display of an numpy array as an image in the notebook

    :param image: the image array
    :param vmax: the value corresponding to the maximum
    :param autoresize: the size of the image below it will be resized

    """
    # TODO complete and shorten
    if browse_axes is not None:

        def browse(**kwargs):
            indexing_list = [slice(None) for _ in range(len(ar.shape))]
            for ba in browse_axes:
                indexing_list[ba] = kwargs[ba]
            display(array_to_img(ar[tuple(indexing_list)], **kwargs))

        return interact(browse, {axis: (0, ar.shape[axis] - 1) for axis in browse_axes})

    elif len(ar.shape) == 2:
        display(array_to_img(ar, **kwargs))
    elif len(ar.shape) == 3:
        # probably RGB if the last dimension is 3
        if ar.shape[2] == 3:
            return array_to_img(ar, **kwargs)

        def browse(i: (0, ar.shape[0] - 1)):
            indexing_list = [slice(None) for _ in range(len(ar.shape))]
            indexing_list[0] = i
            display(array_to_img(ar[tuple(indexing_list)], **kwargs))

        return interact(browse)
    elif len(ar.shape) == 4:

        # probably RGB if the last dimension is 3
        if ar.shape[3] == 3:

            def browse(i: (0, ar.shape[0] - 1)):
                indexing_list = [slice(None) for _ in range(len(ar.shape))]
                indexing_list[0] = i
                display(array_to_img(ar[tuple(indexing_list)], **kwargs))

            return interact(browse)

        def browse(t: (0, ar.shape[0] - 1), z: (0, ar.shape[1] - 1)):
            indexing_list = [slice(None) for _ in range(len(ar.shape))]
            indexing_list[0] = t
            indexing_list[1] = z
            display(array_to_img(ar[tuple(indexing_list)], **kwargs))

        return interact(browse)
    else:
        raise ValueError("Unsupported number of dimensions for display")


def normalise_clip(stack, vmin=None, vmax=None, nmx=255, wins_min=1, wins_max=99.99):
    """ Normalises the stack to a good range for display. If the
    minium and maximum values are not set, it takes the 1st and 99th percentile

    :param stack:
    :param vmin:
    :param vmax:
    :param nmx:
    :return:
    """
    if vmin is None:
        vmin = np.percentile(stack.flatten(), wins_min)
    if vmax is None:
        vmax = np.percentile(stack.flatten(), wins_max)
    return (nmx * 1.0 * (np.clip(stack, vmin, vmax) - vmin) / (vmax - vmin)).astype(
        np.uint8
    )