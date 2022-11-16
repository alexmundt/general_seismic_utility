import matplotlib.pyplot as plt
import picking_class as pck
from picking_class import pick_lines, pick_waveform
# for random data functionality
from numpy.random import default_rng
import numpy as np
from os import listdir
from obspy import read as waveform_read
import pandas as pd



class gui_picker():
    """
    class that connects all the GUI functionality with the picks container
    and reading
    """
    def __init__(self, fig = None, ax = None):
        """
        initialize the fig and ax if needed, the container class and read
        """


        if fig == None or ax == None:
            self.fig, self.ax = plt.subplots()

        self.current_index = 0
        self.right_mode = False
        self.left_mode = False

        # initialize list container for waveform picks
        self.container_list = []
        self.current_data = None

        self.__bind_methods_gui()

    def read_waveforms(self, folder = "waveforms"):
        """
        this function reads all the waveform files from a given directory dir
        and links it to the catalog
        """
        # get contents of the folder using python OS function
        dir = listdir(folder)
        files_num = len(dir)

        self.__build_container_list(files_num)
        for i in range(files_num):
            pick = self.container_list[i]
            filename = f"{folder}/{dir[i]}"
            pick.attach_filename(filename)

        self.num_data = files_num
        self.__call_print_info()
        self.__get_current_data()

    def __on_click(self, event):
        """
        private function gets activated when click event in the figure is noted
        """
        # initialize current values from class instance
        i = self.current_index
        left_mode = self.left_mode
        right_mode = self.right_mode

        if left_mode == True or right_mode == True:
            # ax.plot(event.xdata, event.ydata, marker="x")
            x_pick = pick_lines(event.xdata)
            # get the current pick container
            pick_cont = self.container_list[i]

            if left_mode == True:
                pick_cont.append(x_pick, "left")
            if right_mode == True:
                pick_cont.append(x_pick, "right")
            pick_cont.plot(self.ax)
            # pick_cont_list[i] = pick_cont
            # x_pick.plot(ax)
            # print(pick_cont.return_picks())
            self.fig.canvas.draw()

        # set left_mode and right_mode
        left_mode = False
        right_mode = False

        pass

    def __key_press(self, event):
        """
        private function that handles key press events
        """
        # reset left_mode and right mode
        self.left_mode = False
        self.right_mode = False
        # plt.close(fig)
        # fig, ax = plt.subplots(1)
        print(f"key pressed is: {event.key}")
        # print(len(vals))
        if (event.key == "right") or (event.key == "left"):
            # call the function that changes data to be displayed
            self.__change_displayed_data(event)
        if (event.key == "n"):
            print("N PRESSED - left mode engaged")
            self.left_mode = True
        if (event.key == "m"):
            print("M PRESSED - right mode engaged")
            self.right_mode = True
        if (event.key == "p"):
            print("P PRESSED - print mode engaged")
            self.__call_print_info()
            self.output_to_csv()
        pass

    def __bind_methods_gui(self):
        """
        private method that binds the functionality to the GUI events
        """
        fig = self.fig
        self.mouse_click = self.fig.canvas.mpl_connect('button_press_event',
            self.__on_click)
        self.key_press = self.fig.canvas.mpl_connect("key_press_event",
            self.__key_press)
        print("Binding function called")

    def __call_print_info(self):
        """
        private method that calls the print info
        """
        for item in self.container_list:
            item.print_info()
        # print(len(self.container_list))
        self.__transform_picks_to_ndarray()
        self.__create_filenames_list()

    def __build_container_list(self, num_elements):
        """
        method that builds the container list
        """
        self.container_list = []
        for j in range(num_elements):
            self.container_list.append(pick_waveform())



    def __change_displayed_data(self, event):
        """
        function that changes the data that is currently being displayed
        """
        # initialize values used in this function from the class instance
        i = self.current_index

        if (i < self.num_data-1) and event.key == "right":
            i+= 1
        elif i > 0 and event.key == "left":
            i-= 1

        self.__plot_index(i)

    def __plot_index(self, index):
        """ a private method that plots the given index
        """
        fig = self.fig
        ax = self.ax
        i = index

        # reset the current index
        self.set_current(i)

        ax.clear()
        # plot the current picks
        pick_cont = self.container_list[i]
        pick_cont.plot(ax)

        # plot the current function
        self.__get_current_data()
        time, data = self.current_data_time, self.current_data

        # pick_cont.plot(ax)
        ax.plot(time,data)
        ax.xaxis_date()

        # ax.plot(self.vals[i])

        filename = pick_cont.waveform_filename
        filename = filename.replace(".mseed", "")
        filename = filename.replace("waveforms/","")
        ax.set_title(f"{filename}")
        fig.canvas.draw()
        fig.canvas.flush_events()

    def __set_num_data(self, num):
        """
        private method that sets the properties about the data"""
        self.num_data = num

    def __get_current_data(self):
        """
        a private method that gets the current data either from the
        relevant waveform files or if those do not exist, get randomly created
        values
        """
        i = self.current_index
        current_cont = self.container_list[self.current_index]
        if not current_cont.waveform_filename:
            print(f"no filename on record to read! = {self.container_list}")
            data = self.vals[self.current_index]
            time = np.arange(len(data))
        else:
            read_filename = current_cont.waveform_filename
            time, data  = load_obspy_waveform(read_filename)
        self.current_data_time, self.current_data = time, data

    def __transform_picks_to_ndarray(self):
        """
        a private method that transforms all the picks in the container list
        into a (n,2) ndarray in numpy
        """
        n = len(self.container_list)
        pick_array = np.zeros((n, 2))
        for i, container in enumerate(self.container_list):
            left = container.get_pick("left")
            right = container.get_pick("right")

            pick_array[i] = [left, right]
        self.pick_array = pick_array


    def __create_filenames_list(self):
        """ a private method to create a list of filenames in the container list
        """
        filenames_list = []
        for container in self.container_list:
            filename = container.waveform_filename
            filenames_list.append(filename)
        # print("filenames list:")
        # for item in filenames_list:
        #     print(item)
        self.filenames_list = filenames_list


    def set_current(self, index):
        """
        a method that sets the current values to the index
        """
        self.current_index = index
        # self.current_data = self.vals[self.current_index]

    def show(self):
        """
        method that shows the figure on screen
        """
        # self.fig.show()
        # if self.current_data ==
        # print(type(self.current_data))
        # print(type(self.current_data))
        if not isinstance(self.current_data, np.ndarray):
            self.create_random_data()
        self.__plot_index(self.current_index)
        plt.show()

    def create_random_data(self):
        """
        a method that creates random data to display and show
        """
        rng = default_rng()
        self.vals = rng.random(size=((10,10)))
        self.current_data = self.vals[0]
        self.__set_num_data(len(self.vals))
        self.__build_container_list(len(self.vals))
        # print(self.num_data)

    def output_to_csv(self, filename="output.csv"):
        """ method to output the filenames and associated picks
        """
        self.__transform_picks_to_ndarray()
        self.__create_filenames_list()

        print(self.filenames_list)
        print(self.pick_array)
        # df = pd.DataFrame(data=[self.filenames_list, self.pick_array[:,0],
        #     self.pick_array[:,1] ],
        #     columns = ["filenames", "left", "right"])
        df =  pd.DataFrame(data=self.filenames_list, columns= ["filenames"])
        df["left"]= self.pick_array[:,0]
        df["right"]= self.pick_array[:,1]
        df.to_csv(filename)

def load_obspy_waveform(filename):
    """
    a function that reads a MSEED waveform downloaded from Obspy and outputs
    the files in numpy formats
    """
    st = waveform_read(filename)
    tr = st [0]
    time = tr.times("matplotlib")
    data = tr.data
    return time, data
