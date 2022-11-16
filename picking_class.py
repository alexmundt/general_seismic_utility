
class pick_lines(object):
    """
    a class that stores the properties of location of a horizontal line
    """
    def __init__(self, x_coord=0):
        self.x_coord = x_coord

    def plot(self, ax):
        line = 0
        if self.x_coord != 0:
            ax.axvline(x= self.x_coord, ymin = 0, ymax = 1, color = "red")


class pick_container(object):
    """
    a list like class that stores all picks and plots all of them
    """
    def __init__(self):
        self.container = []
        # self.plot_lines = []

    def append(self, pick_line):
        self.container.append(pick_line)

    def plot(self, ax):
        """
        function that plots the plotlines
        """
        lines_to_be_removed = []
        for line in ax.lines:
            # the picks only have two 2 x-coordinates
            x_data_dimensions = len(line.get_data()[0])
            # check which lines need to removed and only remove the right ones
            if x_data_dimensions == 2:
                lines_to_be_removed.append(line)
        for line in lines_to_be_removed:
            ax.lines.remove(line)
        # remove all further references to the remaining lines
        lines_to_be_removed = []
        for pick_line in self.container:
            if pick_line == None:
                print("No pick to plot")
            else:
                pick_line.plot(ax)

        # print(f"plotlines object = {self.plot_lines}")
        print(f"self.container = {self.container}")

    def return_picks(self):
        """
        a function that outputs a list of picks
        """
        list_output = []
        for item in self.container:
            list_output.append(item.x_coord)
        return list_output

    # def (self)

class pick_waveform(pick_container):
    """
    a subclass of pick_container that only stores 2 picks: left and right
    """

    def __init__(self, filename = None):
        super().__init__()
        self.picks = {"left":pick_lines(), "right":pick_lines()}
        self.container = []
        # attach the filename to the actual container
        self.attach_filename(filename)

    def __update_container(self):
        """
        this function updates container using only the picks stored in
        the self.picks dictionary storing only left and right picks
        """
        self.container = [self.picks["left"], self.picks["right"]]


    def append(self, pickline, place=None):
        """
        this function overwrites the generic pick container append and
        stores the pick in the corresponding place. the function only allows
        "left" or "right" picks
        """
        if place == "left":
            self.picks["left"] = pickline
        elif place == "right":
            self.picks["right"] = pickline
        else:
            print("No picks saved because place information was incorrectly \
            transmitted")
        self.__update_container()

    def attach_filename(self, filename):
        """
        this function is to be called when attaching a filename
        """
        self.waveform_filename = filename

    def print_info(self):
        """
        this function prints the info
        """
        waveform = self.waveform_filename
        left = self.picks["left"]
        right = self.picks["right"]
        # print("###########")
        print(f"Filename of the waveform = {waveform}")
        print(f"Left pick = {left.x_coord} and right pick = {right.x_coord}")
        # print("###########")

    def get_pick(self, side):
        """
        get the pick from the left or right side
        """
        pick = self.picks[side]
        output = pick.x_coord
        return output
