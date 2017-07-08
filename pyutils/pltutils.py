# Plotting and visualization centric helper functions
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import matplotlib.pyplot as plt

def plot_image(image,  msg = ""):
	"""
	Plots an image with an optional message.
	"""
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.imshow(image)
	if msg:
		plt.text(0.95, 0.05, msg, ha='right', va='center', color='w',
		        transform=ax.transAxes)
	plt.grid()
	plt.show()
