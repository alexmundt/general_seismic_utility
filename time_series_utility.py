import numpy as np

def calc_error(f1,f2):
    """
    function that calculates the squared error of two vectors
    """
    error = np.sum((f1-f2)**2.)
    return error

def get_shift_index(f1, f2, pad_num = 0):
    """
    function that gets the index-difference of the most advantageous shift
    """
    # get the length of the time series
    n = len(f1)
    if pad_num == 0:
        # set the padding number to the length of the time series
        pad_num = int(n/4)

    error_data = calc_shift_error(f1, f2, pad_num)

    minimum_index = np.argmin(error_data) - pad_num

    return minimum_index

def calc_shift_error(f1, f2, pad_num):
    """
    helper function that calculates the shift error
    """
    # initialize the errors
    error_data = np.zeros(pad_num * 2)

    # pad both time series with zeros
    f1_padded = np.pad(f1, (pad_num, pad_num), 'constant', constant_values=(0,0))
    f2_padded = np.pad(f2, (pad_num, pad_num), 'constant', constant_values=(0,0))


    for i in range(-pad_num, pad_num):
        j = i + pad_num
        shifted_data = np.roll(f1_padded, i)
        error_data[j] = calc_error(shifted_data, f2_padded)

    return error_data
