from numpy import ndarray
from scipy import signal
import numpy as np
from nptyping import NDArray


def sliding_window(vols: NDArray, ws: int, ss: int = 1) -> NDArray:
    """
    Extract each window values from time series
    :param vols: volumes to take into account, array type with size [n_vols]
    :param ws: Window length in vols
    :param ss: Step size in vols (default=1)
    :return: out, all the sliding windows, array type with shape [n_window, ws]
    """
    if ss is not None:
        ss = ss
    else:
        # no step size was provided. Return non-overlapping windows
        ss = ws
        # calculate the number of windows to return, ignoring left over samples, and allocate memory to contain the
        # samples
    valid = len(vols) - ws
    nw = abs(valid // ss)  # new qty windows possible
    out = np.ndarray((nw, ws), dtype=vols.dtype)  # rows: number of windows, columns: window length

    for i in range(nw):
        # "slide" the window along the samples
        start = i * ss
        stop = start + ws
        out[i] = vols[start: stop]

    return out


def taper(window, ws: int = 60, wtype: str = 'hann'):
    """
    Apply taper window over the signal
    :param window: array of sliding window indices.
    :param ws: window lenght or number of points in the output window. (default : 60s)
    :param wtype: window type (rect, hann, hamming, tukey). (default : hann)
    :return: out, the window
    """
    taper: ndarray = np.zeros(ws)
    if wtype == 'tukey':
        taper = signal.tukey(ws, alpha=0.5, sym=True)
    elif wtype == 'hann':
        taper = signal.hanning(ws, sym=True)
    elif wtype == 'hamming':
        taper = signal.hamming(ws, sym=True)
    elif wtype == 'rect':
        taper = signal.windows.boxcar(ws, sym=True)

    # Removing the average value before tapering (to avoid spurious correlations at the beginning and end of the
    # windows)
    window = window - np.mean(window)
    out = window * taper

    return out


def dynamic_functional_connectivity(data, ws, ss=1, wtype: str = 'hann'):
    """
    Computes Sliding-window time-series per subject per region.
    :param data: Resting state BOLD time-series for subjects. Data array with subjects, # vols, and ROI's.
    shape: [n_subjects, n_vol, n_roi].
    :param ws: Window size in vols
    :param ss: Step size in vols (default=1)
    :param wtype: tapered window function (rect, hann, hamming, tukey). (default : hann)
    :return: swin_ts: sliding window time series. Shape [n_subjects, n_windows, ws, n_roi]
    """
    nsubj = data.shape[0]  # number of subjects
    nvol = data.shape[1]  # number of volumes
    nfeat = data.shape[2]  # number of brain regions
    swin_ts = np.ndarray((nsubj, np.int16(np.ceil((nvol - ws) // ss)), ws, nfeat))
    for idx, s in enumerate(data):
        fulltimewin = np.arange(nvol, dtype='int32')
        swins = sliding_window(vols=fulltimewin, ws=ws, ss=ss)
        n_swin = swins.shape[0]  # number of sliding windows
        swin_ts[idx] = np.empty((n_swin, ws, nfeat))
        for n, curwin in enumerate(swins):
            cur_ts = s[curwin, :]
            swin_ts[idx][n] = np.ndarray((ws, nfeat))
            for i in range(nfeat):
                swin_ts[idx][n][:, i] = taper(cur_ts[:, i], ws, wtype)
    return swin_ts, swin_ts.shape[1]
