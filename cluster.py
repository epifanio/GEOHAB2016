from grass.script import array as garray
from spectral import *
import spectral.io.envi as envi
spectral.settings.show_progress = False
import numpy as np
import matplotlib.pyplot as plt


def img2array(img, npred=8):
    rl = garray.array()
    imagegroup = np.empty((rl.shape[0], rl.shape[1], npred), dtype='float')
    for i,v in enumerate(img[3:]):
        rl.read(v)
        imagegroup[:, :, i] = rl
    return imagegroup

def spectralPlot(c):
    for i in range(c.shape[0]):
        plt.plot(c[i])

def getKmeans(imagegroup='', k=5, samps=150, bands="all"):
    if bands=="all":
        (m1, c1) = kmeans(imagegroup[:, :, :], k, samps)
    if bands!="all":
        (m1, c1) = kmeans(imagegroup[:, :, range(0,bands)], k, samps)
    return (m1, c1)

def writeGarray(m, mapname):
    clust = garray.array()
    clust[...] = m
    clust.write(mapname)
    print("newmap %s written to GRASS MAPSET" % mapname)