from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
from monitor import *
class CrossLinePlot(object):
    def __init__(self):
        self.start_time = time.time()
        self.count      = 0
        self.bar_size   = 10
        self.time_interval = 4
class ShowPlot(object):
    def __init__(self, root):
        self.cross_plot = CrossLinePlot()
        self.wnd = root
    def show_temperature(self,file):
        self.df  =  pd.read_csv(file)
        
class RootWindow(object):
    def __init__(self, shape, locate):
        self.wnd = Tk()
        self.wnd.resizable(width=False,height=False)
        self.wnd.withdraw()
        s_shape = str(shape[0])+'x'+str(shape[1])
        s_locate = '+' + str(locate[0]-shape[0]) + '+' + str(locate[1])
        self.wnd.geometry(s_shape + s_locate)
        self.wnd.title("Multi-Scale & Complex Flow Lab HPC Monitor")
        
        label_local = (0, 5)
        label = Label(self.wnd, text='number of statistical')
        label.place(x=label_local[0], y=label_local[1])

        fig_frame_shape = (shape[0],shape[1]-40)
        fig_frame_local = (0, 40)
        fig_frame = Frame(self.wnd, width=fig_frame_shape[0], 
                                    height=fig_frame_shape[1])
        fig_frame.propagate(0)
        fig_frame.place(x=fig_frame_local[0], y=fig_frame_local[1])
        self.fig_plot = FigurePlot(fig_frame, fig_frame_shape)
    def wnd_update(self):
        self.wnd.update()
        self.wnd.deiconify()
if __name__ == "__main__":
    root = RootWindow((800,400),(500,300))
    second = sleeptime(0,0,10)
    firstname = 'node'
    nodenames = ['80','81','82','83','84','85','86','88','89','72','73','74','75','101','102',
            '103','104','105','106','107','108']
    sugon     = ['192.168.211.90','192.168.211.176']
    threshold = 55
    if not os.path.exists('./log'):
        os.mkdir('./log')
    show_plot = ShowPlot(root)
    while True:
        file = monitor(firstname,nodenames,threshold)
        #monitor_sugon()
        show_plot.show_temperature(file)
        root.wnd_update()
        time.sleep(second)
    root.wnd.mainlop()