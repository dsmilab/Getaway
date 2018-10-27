import os
import posixpath

BASE_PATH = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

DATA_DIR_PATH = posixpath.join(BASE_PATH, '../data/')
SOUND_PATH = posixpath.join(DATA_DIR_PATH, 'sound/')
MAP_PATH = posixpath.join(DATA_DIR_PATH, 'map/')
CONCENTRIC_PATH = posixpath.join(DATA_DIR_PATH, 'concentric/')
SIGNAL_PATH = posixpath.join(DATA_DIR_PATH, 'signal/')
HUD_PATH = posixpath.join(DATA_DIR_PATH, 'hud/')
