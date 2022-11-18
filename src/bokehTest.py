# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 12:41:13 2022

@author: Freddie
"""

import os
from numpy import pi,sin,linspace
from pathlib import Path
from bokeh.plotting import figure, output_file, show

plot = figure(title = "Sine Wave example", x_axis_label='x', y_axis_label='y')
x = linspace(0,2*pi,1000)
y = sin(x)
plot.line(x,y)

outputPath = Path(os.getcwd())
outputPath = outputPath.parent.absolute()
outputPath = os.path.join(outputPath, 'output\\test.html')
output = output_file(outputPath)
show(plot)
#input("Press any key")