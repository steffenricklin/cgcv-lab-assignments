from collections import namedtuple
from PIL import Image


# bridge_image = Image.open("images/castle/bridge.png").convert('RGBA')
# ground_image = Image.open("images/castle/ground.png").convert('RGBA')
# river_image = Image.open("images/castle/river.png").convert('RGBA')
# riverturn_image = Image.open("images/castle/riverturn.png").convert('RGBA')
# road_image = Image.open("images/castle/road.png").convert('RGBA')
# roadturn_image = Image.open("images/castle/roadturn.png").convert('RGBA')
# t_image = Image.open("images/castle/t.png").convert('RGBA')
# tower_image = Image.open("images/castle/tower.png").convert('RGBA')
# wall_image = Image.open("images/castle/wall.png").convert('RGBA')
# wallriver_image = Image.open("images/castle/wallriver.png").convert('RGBA')
# wallroad_image = Image.open("images/castle/wallroad.png").convert('RGBA')
# bridge_image = Image.open("images/castle/bridge.png")
# ground_image = Image.open("images/castle/ground.png")
# river_image = Image.open("images/castle/river.png")
# riverturn_image = Image.open("images/castle/riverturn.png")
# road_image = Image.open("images/castle/road.png")
# roadturn_image = Image.open("images/castle/roadturn.png")
# t_image = Image.open("images/castle/t.png")
# tower_image = Image.open("images/castle/tower.png")
# wall_image = Image.open("images/castle/wall.png")
# wallriver_image = Image.open("images/castle/wallriver.png")
# wallroad_image = Image.open("images/castle/wallroad.png")


# castle_tiles = [
#     Tile('bridge_lr', bridge_image,
#          ('road', 'river', 'road', 'river'), 1/2),
#     Tile('bridge_ud', bridge_image.transpose(Image.ROTATE_90),
#          ('river', 'road', 'river', 'road'), 1/2),
#     Tile('ground', ground_image,
#          ('ground', 'ground', 'ground', 'ground'), 1),
#     Tile('river_ud', river_image,
#          ('ground', 'river', 'ground', 'river'), 1/2),
#     Tile('river_lr', river_image.transpose(Image.ROTATE_90),
#          ('river', 'ground', 'river', 'ground'), 1/2),
#     Tile('riverturn_tr', riverturn_image,
#          ('river', 'river', 'ground', 'ground'), 1/4),
#     Tile('riverturn_tl', riverturn_image.transpose(Image.ROTATE_90),
#          ('ground', 'river', 'river', 'ground'), 1/4),
#     Tile('riverturn_bl', riverturn_image.transpose(Image.ROTATE_180),
#          ('ground', 'ground', 'river', 'river'), 1/4),
#     Tile('riverturn_br', riverturn_image.transpose(Image.ROTATE_270),
#          ('river', 'ground', 'ground', 'river'), 1/4),
#     Tile('road_ud', road_image,
#          ('ground', 'road', 'ground', 'road'), 1/2),
#     Tile('road_lr', road_image.transpose(Image.ROTATE_90),
#          ('road', 'ground', 'road', 'ground'), 1/2),
#     Tile('roadturn_tr', roadturn_image,
#          ('road', 'road', 'ground', 'ground'), 1/4),
#     Tile('roadturn_tl', roadturn_image.transpose(Image.ROTATE_90),
#          ('ground', 'road', 'road', 'ground'), 1/4),
#     Tile('roadturn_bl', roadturn_image.transpose(Image.ROTATE_180),
#          ('ground', 'ground', 'road', 'road'), 1/4),
#     Tile('roadturn_br', roadturn_image.transpose(Image.ROTATE_270),
#          ('road', 'ground', 'ground', 'road'), 1/4),         
#     Tile('t_d', t_image,
#          ('ground', 'ground', 'ground', 'road'), 1/4),
#     Tile('t_r', t_image.transpose(Image.ROTATE_90),
#          ('road', 'ground', 'ground', 'ground'), 1/4),
#     Tile('t_u', t_image.transpose(Image.ROTATE_180),
#          ('ground', 'road', 'ground', 'ground'), 1/4),
#     Tile('t_l', t_image.transpose(Image.ROTATE_270),
#          ('ground', 'ground', 'road', 'ground'), 1/4),
#     Tile('tower', tower_image,
#          ('wall', 'wall', 'wall', 'wall'), 1),
#     Tile('wall_ud', wall_image,
#          ('ground', 'wall', 'ground', 'wall'), 1/2),
#     Tile('wall_lr', wall_image.transpose(Image.ROTATE_90),
#          ('wall', 'ground', 'wall', 'ground'), 1/2),
#     Tile('wallriver_ud', wallriver_image,
#          ('river', 'wall', 'river', 'wall'), 1/2),
#     Tile('wallriver_lr', wallriver_image.transpose(Image.ROTATE_90),
#          ('wall', 'river', 'wall', 'river'), 1/2),
#     Tile('wallroad_ud', wallroad_image,
#          ('road', 'wall', 'road', 'wall'), 1/2),
#     Tile('wallroad_lr', wallroad_image.transpose(Image.ROTATE_90),
#          ('wall', 'road', 'wall', 'road'), 1/2),
# ]



images = {
    "bridge":    Image.open("images/castle/bridge.png"),
    "ground":    Image.open("images/castle/ground.png"),
    "river":     Image.open("images/castle/river.png"),
    "riverturn": Image.open("images/castle/riverturn.png"),
    "road":      Image.open("images/castle/road.png"),
    "roadturn":  Image.open("images/castle/roadturn.png"),
    "t":         Image.open("images/castle/t.png"),
    "tower":     Image.open("images/castle/tower.png"),
    "wall":      Image.open("images/castle/wall.png"),
    "wallriver": Image.open("images/castle/wallriver.png"),
    "wallroad":  Image.open("images/castle/wallroad.png")
}

Tile = namedtuple('Tile', ('name', 'bitmap', 'sides', 'weight'))

# 4 constraints: wall/tower to wall/tower, road/bridge to road/bridge, river to river, ground to ground

castle_neighbors = {
    'bridge_lr':    ('road',   'river',  'road',   'river'),
    'bridge_ud':    ('river',  'road',   'river',  'road'),
    'ground':       ('ground', 'ground', 'ground', 'ground'),
    'river_ud':     ('ground', 'river',  'ground', 'river'),
    'river_lr':     ('river',  'ground', 'river',  'ground'),
    'riverturn_tr': ('river',  'river',  'ground', 'ground'),
    'riverturn_tl': ('ground', 'river',  'river',  'ground'),
    'riverturn_bl': ('ground', 'ground', 'river',  'river'),
    'riverturn_br': ('river',  'ground', 'ground', 'river'),
    'road_ud':      ('ground', 'road',   'ground', 'road'),
    'road_lr':      ('road',   'ground', 'road',   'ground'),
    'roadturn_tr':  ('road',   'road',   'ground', 'ground'),
    'roadturn_tl':  ('ground', 'road',   'road',   'ground'),
    'roadturn_bl':  ('ground', 'ground', 'road',   'road'),
    'roadturn_br':  ('road',   'ground', 'ground', 'road'),
    't_d':          ('ground', 'ground', 'ground', 'road'),
    't_r':          ('road',   'ground', 'ground', 'ground'),
    't_u':          ('ground', 'road',   'ground', 'ground'),
    't_l':          ('ground', 'ground', 'road',   'ground'),
    'tower':        ('wall',   'wall',   'wall',   'wall'), 
    'wall_ud':      ('ground', 'wall',   'ground', 'wall'),
    'wall_lr':      ('wall',   'ground', 'wall',   'ground'),
    'wallriver_ud': ('river',  'wall',   'river',  'wall'),
    'wallriver_lr': ('wall',   'river',  'wall',   'river'),
    'wallroad_ud':  ('road',   'wall',   'road',   'wall'),
    'wallroad_lr':  ('wall',   'road',   'wall',   'road')
}

weights = {
    'bridge_lr':    0.50,
    'bridge_ud':    0.50,
    'ground':       1.00,
    'river_ud':     0.50,
    'river_lr':     0.50,
    'riverturn_tr': 0.25,
    'riverturn_tl': 0.25,
    'riverturn_bl': 0.25,
    'riverturn_br': 0.25,
    'road_ud':      0.50,
    'road_lr':      0.50,
    'roadturn_tr':  0.25,
    'roadturn_tl':  0.25,
    'roadturn_bl':  0.25,
    'roadturn_br':  0.25,
    't_d':          0.25,
    't_r':          0.25,
    't_u':          0.25,
    't_l':          0.25,
    'tower':        1.00, 
    'wall_ud':      0.50,
    'wall_lr':      0.50,
    'wallriver_ud': 0.50,
    'wallriver_lr': 0.50,
    'wallroad_ud':  0.50,
    'wallroad_lr':  0.50 
}


def get_tiles(is_bool=False):
    c_tiles = [Tile(k, images[k.split('_')[0]].convert('RGBA'), neighbors, weights[k]) for k, neighbors in castle_neighbors.items()]
    return c_tiles
#     return castle_tiles
