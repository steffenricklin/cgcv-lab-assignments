# %%
import random
import io
import base64
from collections import namedtuple
import numpy as np
from PIL import Image, ImageDraw
from IPython import display
import matplotlib.pyplot as plt

# %%
def blend_many(ims):
    """
    Blends a sequence of images.
    """
    current, *ims = ims
    for i, im in enumerate(ims):
        current = Image.blend(current, im, 1/ (i+2))
    return current

# %%
def blend_tiles(choices, tiles):
    """
    Given a list of states (True if ruled out, False if not) for each tile,
    and a list of tiles, return a blend of all the tiles that haven't been
    ruled out.
    """
    to_blend = [tiles[i].bitmap for i in range(len(choices)) if choices[i]]
    return blend_many(to_blend)

# %%
def show_state(potential, tiles):
    """
    Given a list of states for each tile for each position of the image, return
    an image representing the state of the global image.
    """
    rows = []
    for row in potential:
        rows.append([np.asarray(blend_tiles(t, tiles)) for t in row])

    rows = np.array(rows)
    n_rows, n_cols, tile_height, tile_width, _ = rows.shape
    images = np.swapaxes(rows, 1, 2)
    return Image.fromarray(images.reshape(n_rows*tile_height, n_cols*tile_width, 4))

# %%
def find_true(array):
    """
    Like np.nonzero, except it makes sense.
    """
    transform = int if len(np.asarray(array).shape) == 1 else tuple
    return list(map(transform, np.transpose(np.nonzero(array))))

# %%
Tile = namedtuple('Tile', ('name', 'bitmap', 'sides', 'weight'))

# %%
size = 10
dirs = {
    'tl': (0, 0),
    'tr': (size, 0),
    'bl': (0, size),
    'br': (size, size),
    'mid': (size/2, size/2)
}

def make_wang_tile(right, up, left, down):
    im = Image.new(mode='RGBA', size=(size, size))
    draw = ImageDraw.Draw(im)
    draw.polygon([dirs['tr'], dirs['mid'], dirs['br']], fill=right)
    draw.polygon([dirs['tl'], dirs['mid'], dirs['tr']], fill=up)
    draw.polygon([dirs['tl'], dirs['mid'], dirs['bl']], fill=left)
    draw.polygon([dirs['bl'], dirs['mid'], dirs['br']], fill=down)
    return im

wang_set = {

    't0': ('red', 'red', 'green', 'red'),
    't1': ('red', 'blue', 'green', 'blue'),
    't2': ('green', 'red', 'green', 'green'),
    't3': ('blue', 'white', 'blue', 'red'),
    't4': ('blue', 'blue', 'blue', 'white'),
    't5': ('white', 'white', 'white', 'red'),
    't6': ('green', 'red', 'white', 'blue'),
    't7': ('white', 'blue', 'red', 'blue'),
    't8': ( 'red', 'blue','red', 'white'),
    't9': ('green', 'green', 'red', 'blue'),
    't10': ('white', 'red', 'green', 'red')
}

# %%
from enum import Enum, auto

class Direction(Enum):
    RIGHT = 0; UP = 1; LEFT = 2; DOWN = 3
    
    def reverse(self):
        return {Direction.RIGHT: Direction.LEFT,
                Direction.LEFT: Direction.RIGHT,
                Direction.UP: Direction.DOWN,
                Direction.DOWN: Direction.UP}[self]

# %%
def neighbors(location, height, width):
    res = []
    x, y = location
    if x != 0:
        res.append((Direction.UP, x-1, y))
    if y != 0:
        res.append((Direction.LEFT, x, y-1))
    if x < height - 1:
        res.append((Direction.DOWN, x+1, y))
    if y < width - 1:
        res.append((Direction.RIGHT, x, y+1))
    return res

# %%
def backtrack(potential, images):
    old_potential = potential.copy()
    # display.display(show_state(potential, tiles))
    images.append(show_state(potential, tiles))

    # Done
    if done(potential):
        print('It is done.')
        out = io.BytesIO()
        images[0].save(out, format='gif', save_all=True, append_images=images[1:],
               duration=50, loop=0)
        return True
    else:
        # Otherwise get all candidate locations
        candidates = get_candidates(potential)
        for candidate in candidates:

            ### Prepare

            # Find indices of all candidate tiles
            nonzero = find_true(potential[candidate])

            # choose a random one according to weights
            if len(nonzero) > 0:
                tile_probs = weights[nonzero] / sum(weights[nonzero])
                nonzero = np.random.choice(nonzero, p=tile_probs, size=len(nonzero), replace=False)

            for tile in nonzero:
                potential[candidate] = False
                potential[candidate][tile] = True
                propagate_bt(potential, candidate)

                if np.any(potential[candidate]):
                    
                    ### Recurse

                    solved = backtrack(potential, images)
                    if solved:
                        return True

                ### Repair

                potential = old_potential


def done(potential):
    return np.sum(potential) == potential.shape[0] * potential.shape[1]



def get_candidates(potential):
    '''
    Returns a list of all coordinates which can be collapsed in 
    order max constrained to min constrained 
    '''
    # 2d array where each entry is the number of choices
    num_choices = np.sum(potential, axis=2, dtype='float32')

    # if there's only one choice, set it to inf (one choice is no choice)
    num_choices[num_choices == 1] = np.inf
    
    if np.all(num_choices) == np.inf: 
        return None

    # get the indexes in order of the sums, in ascending order
    candidate_locations = np.unravel_index(np.argsort(num_choices, axis=None), num_choices.shape)
    candidate_locations = list(zip(*candidate_locations))
    return candidate_locations


def add_constraint_bt(potential, location, incoming_direction, possible_tiles):
    neighbor_constraint = {t.sides[incoming_direction.value] for t in possible_tiles}
    outgoing_direction = incoming_direction.reverse()
    changed = False
    for i_p, p in enumerate(potential[location]):
        if not p:
            continue
        if tiles[i_p].sides[outgoing_direction.value] not in neighbor_constraint:
            potential[location][i_p] = False
            changed = True
    return changed


def propagate_bt(potential, start_location):

    height, width = potential.shape[:2]
    
    # Initialise grid of who needs an update; initially only the start loc
    needs_update = np.full((height, width), False)
    needs_update[start_location] = True
    
    while np.any(needs_update):

        # While there is still a location that needs an update, 
        # initialise a similar grid for the neighbors
        needs_update_next = np.full((height, width), False)

        # Get all the locations that need an update
        locations = find_true(needs_update)
        for location in locations:
            possible_tiles = [tiles[n] for n in find_true(potential[location])]
            for neighbor in neighbors(location, height, width):
                neighbor_direction, neighbor_x, neighbor_y = neighbor
                neighbor_location = (neighbor_x, neighbor_y)
                
                # Add a constraint to the neighbor location; update the potential, keep going
                was_updated = add_constraint_bt(potential, neighbor_location,
                                             neighbor_direction, possible_tiles)
                needs_update_next[neighbor_location] |= was_updated 
        needs_update = needs_update_next


# %%

gridsize = 30
tiles = [Tile(k, make_wang_tile(*v), v, 1) for k,v in wang_set.items()]
weights = np.asarray([t.weight for t in tiles])
potential = np.full((gridsize, gridsize, len(tiles)), True)
display.display(show_state(potential, tiles))
images = [show_state(potential, tiles)]
backtrack(potential, images)

# %%
out = io.BytesIO()
images[0].save(out, format='gif', save_all=True, append_images=images[1:],
               duration=50, loop=0)
images[-1]

# %%
import base64
from IPython import display
display.HTML('<img src="data:image/gif;base64,{0}">'
             .format(base64.b64encode(out.getvalue()).decode('utf8')))
# %%
# images[0].save('wang_bt.gif', format='gif', save_all=True, append_images=images[1:],
#                duration=50, loop=0)


# %%

# Get an image and put it in numpy
image = Image.open('Flowers.png')
display.display(image)
bitmap = np.asarray(image)

def tile_image(bitmap, n=3):
    
    tiles = np.zeros(bitmap.shape + (n,n))
    bm_width, bm_height, _ = bitmap.shape
    padded = np.pad(bitmap, ((0, n-1), (0, n-1), (0,0)), mode='wrap')
    for x in range(bm_width):
        for y in range(bm_height):
            tiles[x, y] = padded[x:x+n, y:y+n, :]

    return tiles


def assign_weights(tiles):
    unique_elements, counts_elements = np.unique(tiles, return_counts=True)

def show_tiles(tiles):
    fig, ax = plt.subplots(*bitmap.shape[:2])
    for x in range(bitmap.shape[0]):
        for y in range(bitmap.shape[1]):
            ax[x,y].imshow(tiles[x,y].astype(np.uint8))
            ax[x,y].axis('off')
    plt.show()


# image2 = Image.fromarray(data) # back to PIL
# %%
