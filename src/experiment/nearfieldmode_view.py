from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy
import tables

## read file
nfsFile = tables.openFile('D1C-common-50Ohm-3GHz.h5',mode = 'r')

xGrid = nfsFile.getNode(nfsFile.root,'xCoords')
yGrid = nfsFile.getNode(nfsFile.root,'yCoords')
complexVoltagesGrid = nfsFile.getNode(nfsFile.root,'voltage')

## plot data
fig = plt.figure()
ax = fig.gca(projection='3d')

zGrid = numpy.real(complexVoltagesGrid)
surf = ax.plot_surface(xGrid, yGrid, zGrid, rstride=1, cstride=1, cmap=cm.coolwarm,
        linewidth=0, antialiased=False)
#ax.set_zlim(-1.01, 1.01)

#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()