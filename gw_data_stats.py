"""
gw_data_stats
SharedSolar
By: Mitchell Lee
Began on February 22, 2013
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd


# Datamap of any DataFrame
def data_map(wh,color):

	cmap = colors.ListedColormap(['white', color])
	fig = plt.figure()
	densityplot = fig.add_subplot(1,1,1)
	densityplot.spy(wh, aspect = 'auto', cmap = cmap)
	densityplot.set_xticks(range(0,np.shape(wh)[1]))	
	densityplot.set_xticklabels(wh.columns)
	densityplot.set_yticks(range(0,np.shape(wh)[0],750))
	densityplot.set_yticklabels(wh.index[0:np.shape(wh)[0]:750])
	densityplot.set_xlabel('Mains and Circuits')
	densityplot.set_ylabel('Date and Time')
	densityplot.set_title('GW Data map')
	plt.show()

#	Datamap of to DFs to show overlap
def data_map_comp(wh,demdata,color1,color2):
	import numpy as np
	import matplotlib.pyplot as plt
	from matplotlib import colors
	import pandas as pd

	demdata = pd.DataFrame(demdata, index = wh.index,columns = wh.columns)
	cmap1 = colors.ListedColormap(['white', color1])
	cmap2 = colors.ListedColormap(['white', color2])
	fig = plt.figure()
	densityplot = fig.add_subplot(1,1,1)
	densityplot.spy(demdata, aspect = 'auto',cmap = cmap2)		
	densityplot.spy(wh, aspect = 'auto', cmap = cmap1, alpha = 0.5)
	densityplot.set_xticks(range(0,np.shape(wh)[1]))	
	densityplot.set_xticklabels(wh.columns)
	densityplot.set_yticks(range(0,np.shape(wh)[0],750))
	densityplot.set_yticklabels(wh.index[0:np.shape(wh)[0]:750])
	densityplot.set_xlabel('Mains and Circuits')
	densityplot.set_ylabel('Date and Time')
	densityplot.set_title('GW Data map')
	plt.show()

