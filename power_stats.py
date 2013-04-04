import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd

def open_power_ts(circuit):
	'''open a plot of mains or circuits timeseries of power data in watts. When in Ubuntu change
	path to appropriate location'''
	
	ts_path = 'C:/Users/Mitchell/Documents/Shared_Solar/Shared_Solar_database/csv_flat_files_minute/DFlist/'
	ts = pd.read_csv(ts_path + circuit + '_min.csv', delimiter = ';', index_col = 0, parse_dates = True)
	ts[ts > ts.std()*5. + ts.mean()] = np.nan
	return ts