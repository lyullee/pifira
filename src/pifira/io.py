"""
pifira.io
=========
Lightweight loaders for user-supplied CSV files.

No experimental data are bundled with pifira. These helpers parse the two
common file shapes produced by GL840-type dataloggers, but any pipeline that
yields ``(time, pressure)`` and ``(time, temperatures)`` arrays works with the
rest of the library. Bring your own data.
"""

from __future__ import annotations

from io import StringIO

import numpy as np
import pandas as pd

_ENCODINGS = ("utf-8-sig", "cp949", "euc-kr", "utf-8", "latin-1")


def _read_text(path):
    for enc in _ENCODINGS:
        try:
            return open(path, encoding=enc).read().replace("\r", "")
        except (UnicodeDecodeError, UnicodeError):
            continue
    return open(path, encoding="utf-8", errors="ignore").read().replace("\r", "")


def load_pressure_csv(path, time_col=2, value_col=3, header_scan=True):
    """Load a pressure CSV -> (time_s, pressure).

    By default expects columns [index, datetime, seconds, pressure]; the data
    body is detected as the first row whose first field is numeric.

    Parameters
    ----------
    path : str
    time_col, value_col : int
        Column indices for time [s] and pressure.
    header_scan : bool
        If True, auto-detect the first numeric data row.
    """
    lines = _read_text(path).split("\n")
    if header_scan:
        start = next(i for i, ln in enumerate(lines)
                     if ln.split(",")[0].strip().replace(".", "", 1).isdigit())
    else:
        start = 0
    df = pd.read_csv(StringIO("\n".join(lines[start:])), header=None,
                    engine="python")
    t = pd.to_numeric(df.iloc[:, time_col], errors="coerce").values
    v = pd.to_numeric(df.iloc[:, value_col], errors="coerce").values
    ok = ~(np.isnan(t) | np.isnan(v))
    return t[ok], v[ok]


def load_temperature_csv(path, n_channels=10, data_start_row=2):
    """Load a multi-channel temperature CSV -> (time_s, DataFrame[CH1..CHn]).

    Expects columns [index, datetime, seconds, CH1..CHn, ...]. Channel labels
    in the header (e.g. ``CH3(front-centre)``) are ignored here; positions are
    assigned by the caller.
    """
    lines = _read_text(path).split("\n")
    names = ["no", "dt", "sec"] + [f"CH{i}" for i in range(1, n_channels + 1)]
    df = pd.read_csv(StringIO("\n".join(lines[data_start_row:])),
                    header=None, names=names, engine="python")
    df = df[pd.to_numeric(df["no"], errors="coerce").notna()].reset_index(drop=True)
    for ch in [f"CH{i}" for i in range(1, n_channels + 1)]:
        df[ch] = pd.to_numeric(df[ch], errors="coerce")
    t = pd.to_numeric(df["sec"], errors="coerce").values
    return t, df
