from collections import namedtuple
from PIL import Image

Tile = namedtuple('Tile', ('name', 'bitmap', 'sides', 'weight'))

bridge_image = Image.open("images/castle/bridge.png")
ground_image = Image.open("images/castle/ground.png")
river_image = Image.open("images/castle/river.png")
riverturn_image = Image.open("images/castle/riverturn.png")
road_image = Image.open("images/castle/road.png")
roadturn_image = Image.open("images/castle/roadturn.png")
t_image = Image.open("images/castle/t.png")
tower_image = Image.open("images/castle/tower.png")
wall_image = Image.open("images/castle/wall.png")
wallriver_image = Image.open("images/castle/wallriver.png")
wallroad_image = Image.open("images/castle/wallroad.png")

tile_names = [
    'bridge_lr', 'bridge_ud', 
    'ground', 
    'river_ud', 'river_lr', 
    'riverturn_tr', 'riverturn_tl', 'riverturn_bl', 'riverturn_br',
    'road_ud', 'road_lr', 
    'roadturn_tr', 'roadturn_tl', 'roadturn_bl', 'roadturn_br', 
    't_d', 't_r', 't_u', 't_l',
    'tower', 
    'wall_ud', 'wall_lr', 
    'wallriver_ud', 'wallriver_lr', 
    'wallroad_ud', 'wallroad_lr']

# 4 constraints: wall/tower to wall/tower, road/bridge to road/bridge, river to river, ground to ground


# tile_sides = [[  # bridge lr
#     False, False,  # bridge lr/ud
#     False,         # ground
#     False, False,  # river ud/lr
#     False, False, False, False,  # riverturn tr/tl/bl/br
#     False, False,  # road ud/lr
#     False, False, False, False,  # roadturn  tr/tl/bl/br
#     False, False, False, False,  # road "t"-section d/r/u/l
#     False,         # tower 
#     False, False,  # wall      ud/lr
#     False, False,  # wallriver ud/lr
#     False, False   # wallroad  ud/lr
# ], [  
# ]]
castle_tiles = [
    Tile('bridge_lr', bridge_image,
         ['road', 'river', 'road', 'river'], 1/2),
    Tile('bridge_ud', bridge_image.transpose(Image.ROTATE_90),
         ['river', 'road', 'river', 'road'], 1/2),
    Tile('ground', ground_image,
         ['ground', 'ground', 'ground', 'ground'], 1),
    Tile('river_ud', river_image,
         ['ground', 'river', 'ground', 'river'], 1/2),
    Tile('river_lr', river_image.transpose(Image.ROTATE_90),
         ['river', 'ground', 'river', 'ground'], 1/2),
    Tile('riverturn_tr', riverturn_image,
         ['river', 'river', 'ground', 'ground'], 1/4),
    Tile('riverturn_tl', riverturn_image.transpose(Image.ROTATE_90),
         ['ground', 'river', 'river', 'ground'], 1/4),
    Tile('riverturn_bl', riverturn_image.transpose(Image.ROTATE_180),
         ['ground', 'ground', 'river', 'river'], 1/4),
    Tile('riverturn_br', riverturn_image.transpose(Image.ROTATE_270),
         ['river', 'ground', 'ground', 'river'], 1/4),
    Tile('road_ud', road_image,
         ['ground', 'road', 'ground', 'road'], 1/2),
    Tile('road_lr', road_image.transpose(Image.ROTATE_90),
         ['road', 'ground', 'road', 'ground'], 1/2),
    Tile('roadturn_tr', roadturn_image,
         ['road', 'road', 'ground', 'ground'], 1/4),
    Tile('roadturn_tl', roadturn_image.transpose(Image.ROTATE_90),
         ['ground', 'road', 'road', 'ground'], 1/4),
    Tile('roadturn_bl', roadturn_image.transpose(Image.ROTATE_180),
         ['ground', 'ground', 'road', 'road'], 1/4),
    Tile('roadturn_br', roadturn_image.transpose(Image.ROTATE_270),
         ['road', 'ground', 'ground', 'road'], 1/4),         
    Tile('t_d', t_image,
         ['ground', 'ground', 'ground', 'road'], 1/4),
    Tile('t_r', t_image.transpose(Image.ROTATE_90),
         ['road', 'ground', 'ground', 'ground'], 1/4),
    Tile('t_u', t_image.transpose(Image.ROTATE_180),
         ['ground', 'road', 'ground', 'ground'], 1/4),
    Tile('t_l', t_image.transpose(Image.ROTATE_270),
         ['ground', 'ground', 'road', 'ground'], 1/4),
    Tile('tower', tower_image,
         ['wall', 'wall', 'wall', 'wall'], 1),
    Tile('wall_ud', wall_image,
         ['ground', 'wall', 'ground', 'wall'], 1/2),
    Tile('wall_lr', wall_image.transpose(Image.ROTATE_90),
         ['wall', 'ground', 'wall', 'ground'], 1/2),
    Tile('wallriver_ud', wallriver_image,
         ['river', 'wall', 'river', 'wall'], 1/2),
    Tile('wallriver_lr', wallriver_image.transpose(Image.ROTATE_90),
         ['wall', 'river', 'wall', 'river'], 1/2),
    Tile('wallroad_ud', wallroad_image,
         ['road', 'wall', 'road', 'wall'], 1/2),
    Tile('wallroad_lr', wallroad_image.transpose(Image.ROTATE_90),
         ['wall', 'road', 'wall', 'road'], 1/2),
]

def get_tiles():
    
    return castle_tiles
