from os.path import expanduser, realpath, isfile
from random import shuffle
import errno
from os import walk, symlink, remove, getenv
from subprocess import Popen
from .color_parser import *
from .make_sample import *
from .file_list import FileList

WAL_DIR = expanduser( '~' ) + "/.wallpapers/"
SAMPLE_DIR = WAL_DIR + "sample/"
CACHE_DIR = WAL_DIR + "cache/"
XRES_DIR = WAL_DIR + "xres/"

def create_theme(filepath):
    call( 'wal -i ' + filepath, shell=True )
    filename = filepath.split("/").pop()
    color_list = read_colors(filename)
    create_sample(color_list, f=SAMPLE_DIR + filename + '.sample.png')

def set_theme(filename, cs_file):
    if(isfile(WAL_DIR + filename)):
        call( 'wal -si ' + WAL_DIR + filename, shell=True )
        init_file = open( WAL_DIR +'wp_init.sh', 'w' )
        init_file.writelines( [ '#!/bin/bash\n', 'wpg -s ' + filename + ' ' + cs_file] )
        init_file.close()
        Popen( [ 'chmod', '+x', WAL_DIR + 'wp_init.sh' ] )
        call( [ 'xrdb', '-merge', expanduser('~') + '/.Xresources'] )
        call( [ 'xrdb', '-merge', XRES_DIR + cs_file + '.Xres'] )
        try:
            symlink(WAL_DIR + filename, WAL_DIR + ".current")
        except OSError as e:
            if e.errno == errno.EEXIST:
                remove(WAL_DIR + ".current")
                symlink(WAL_DIR + filename, WAL_DIR + ".current")
            else:
                raise e
    else:
        print("no such file, available files:")
        show_wallpapers()

def remove_theme(filename):
    remove(WAL_DIR + filename)
    remove(SAMPLE_DIR + filename + ".sample.png")
    remove(CACHE_DIR + filename + ".col")
    remove(XRES_DIR + filename + ".Xres")

def show_wallpapers():
    files = FileList(WAL_DIR)
    files.show_list()

def show_current():
    image = realpath(WAL_DIR + '.current').split('/').pop()
    print(image)

def shuffle_colors(filename):
    if(isfile(WAL_DIR + filename)):
        colors = read_colors(filename)
        shuffled_colors = colors[1:8]
        shuffle(shuffled_colors)
        colors = colors[:1] + shuffled_colors + colors[8:]
        create_sample(colors)
        write_colors(filename, colors)