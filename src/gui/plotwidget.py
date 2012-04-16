from matplotlibwidget import MatplotlibWidget
from matplotlib import pyplot




class PlotWidget(MatplotlibWidget):
    def __init__(self,parent=None):
        MatplotlibWidget.__init__(self,parent)
        self.figure.set_facecolor(str(self.parent().palette().background().color().name()))

#        font = {'family':'serif', 
#                'serif':'Bookman', 
#                'weight':'normal',
#                'size':8}    
#        pyplot.rc('font', **font)
#        pyplot.rc('font', family='serif', serif='Times New Roman', weight='normal',size=11)
        parentFontSize = self.parent().font().pointSize()
        assert parentFontSize > 5
        pyplot.rc('font', family='sans-serif', weight='normal',size=parentFontSize)
#        pyplot.rc('font', family='serif', serif='palatino', weight='normal',size=11)
#        pyplot.rc('text', usetex=True)
        
#        def paperStyleGraph():
#            pyplot.grid(True,which='major')
#            pyplot.box(False)
#            pyplot.tick_params(which='both',direction='out',top='off',right='off')
#            pyplot.axvline(x=pyplot.xlim()[0],color='k')
#            pyplot.axhline(y=pyplot.ylim()[0],color='k',clip_on=False)
        
if __name__ == '__main__':
    test = PlotWidget()