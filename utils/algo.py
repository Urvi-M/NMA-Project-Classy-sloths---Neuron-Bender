def sliding_window(data, win, step=None):
    """
    win: window size
    step: overlap 
    """
    if step == None: 
        step = win # no overlap
    nt = len(data) # number of time points
    windows = []
    n = int((nt-win+1)/step) #number of windows

    for i in range(n):
        print('\n', i*step,' ', i*step + win)
        windows.append( data[i*step:i*step + win] )
    return windows