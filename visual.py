from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from monitor import *
class FigurePlot(object):
    def __init__(self, root, shape):
        self.wnd = root

        fig = Figure()

        plot_frame = Frame(self.wnd, width=shape[0], height=shape[1], bg='green')
        plot_frame.propagate(0)
        plot_frame.pack(side=TOP, fill=BOTH)
        #--------------------------------------------------------------
        self.canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        #--------------------------------------------------------------
        self.axis1 = fig.add_subplot(111)
        """
        self.axis1.set_ylim((-10,10))    #set the Y-axis interval
        self.axis1.yaxis.set_minor_locator(MultipleLocator(2))
        self.axis1.yaxis.set_major_locator(MultipleLocator(5))
        self.axis1.tick_params(labelsize=7)
        self.axis1.grid(True, which='minor', axis='y', c='c', linestyle='-.', 
                                                            linewidth=0.2)    #
#         self.axis1.get_yaxis().set_visible(False)    #close the ordinate
        self.axis1.get_xaxis().set_visible(False)    #close the ordinate
        self.axis1.spines['right'].set_visible(False)    #close axes
        self.axis1.xaxis.set_ticks_position('top')
        self.axis1.spines['top'].set_position(('data', 0)) 
        """
class CrossLinePlot(object):
    def __init__(self):
        self.start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
class ShowPlot(object):
    def __init__(self, root):
        self.cross_plot = CrossLinePlot()
        self.wnd = root
    def show_temperature(self,file,firstname,nodenames):
        df  =  pd.read_csv(file)
        start_time = self.cross_plot.start_time
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.wnd.fig_plot.axis1.cla()
        for nodename in nodenames:
            tag = firstname+nodename
            node_temp = df.loc[df['node']==tag]
            self.wnd.fig_plot.axis1.plot(x=node_temp['time'],y=node_temp['max_temp'],label=tag)
        self.wnd.fig_plot.axis1.legend(ncol=4,mode='expand')
        self.wnd.fig_plot.axis1.text(-0.1,0.5,now_time)
        self.wnd.fig_plot.canvas.draw()

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
    nodenames = ['80','81','82','84','85','86','88','72','73','74','75','101','102',
            '103','104','105','106','107','108']
    sugon     = ['192.168.211.90','192.168.211.176']
    threshold = 55
    if not os.path.exists('./log'):
        os.mkdir('./log')
    show_plot = ShowPlot(root)
    while True:
        file = monitor(firstname,nodenames,threshold)
        #monitor_sugon()
        show_plot.show_temperature(file,firstname,nodenames)
        root.wnd_update()
        time.sleep(second)
    root.wnd.mainlop()