from matplotlib.dates import num2date
from obspy.core import UTCDateTime


def time_mat2UTC(time):
    """
    processes a given time in matplotlib numerical format to UTCDateTime from
    obspy

    time: numpy.float64
    """
    # first convert into datetime.datetime format
    time_dtdt = num2date(time)

    # then convert into UTCDateTime format
    time_utc = UTCDateTime(time_dtdt)

    return time_utc
