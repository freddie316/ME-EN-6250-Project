#output_file-to save the layout in file, show-display the layout , output_notebook-to configure the default output state  to generate the output in jupytor notebook.
#from bokeh.io import output_file, show, output_notebook
#ColumnDataSource makes selection of the column easier and Select is used to create drop down
from bokeh.models import ColumnDataSource, Select
#Figure objects have many glyph methods that can be used to draw vectorized graphical glyphs. example of glyphs-circle, line, scattter etc.
from bokeh.plotting import figure
#To create intractive plot we need this to add callback method.
from bokeh.models import CustomJS
#This is for creating layout
from bokeh.layouts import column, row, gridplot
from bokeh.models import CustomJS, Dropdown, AutocompleteInput, DateRangeSlider, CheckboxGroup
from bokeh.plotting import figure, output_file, show
import numpy as np
from datetime import date
import os
from pathlib import Path

outputPath = Path(os.getcwd())
outputPath = outputPath.parent.absolute()
outputPath = os.path.join(outputPath, 'output\\covid-dashboard.html')
output = output_file(outputPath)


# TODO - The plot is used in every section, change so each display has its own figures
plot = figure(title = "Sine Wave example", x_axis_label='x', y_axis_label='y')
x = np.linspace(0,2*np.pi,1000)
y = np.sin(x)
plot.line(x,y)
# TODO - create the big display plot
display_big = plot

# TODO - update continent-list.txt to include valid continents and countries
with open('continent-list.txt') as continent_list:
    data = continent_list.read()
    valid_continents = data.split('\n')

# TODO - add functionality to Dropdown menu to update plots
zoomed_continents = Dropdown(label = "Continent Select", menu = valid_continents)
display_zoomed = column(zoomed_continents, plot)

# TODO - change to unique country-list.txt file with just the countries we scraped
with open('country-list-WOM.txt') as country_list:
    data = country_list.read()
    valid_countries = data.split('\n')

# TODO - add JS functions to each of these widgets
interactive_countries = AutocompleteInput(title="Enter a Country:", completions=valid_countries)
interactive_dates = DateRangeSlider(value=(date(2022, 12, 6), date(2022, 12, 8)),
                                    start=date(2022, 12, 6), end=date(2022, 12, 8))
interactive_stats = CheckboxGroup(labels = ['Deaths','Death Rate','Deaths per Million', 'Death rate per Million'], active = [0,1])
interactive_widgets = column(interactive_countries, interactive_dates, interactive_stats)
# TODO - change plot to be whatever we're actually using for this
display_interactive = row(interactive_widgets,plot)

## This section puts them together
layout = column(row(display_big,display_zoomed),display_interactive)
#layout = gridplot([[display_big, display_zoomed],[display_interactive, None]])  # creating the layout
show(layout)  # displaying the layout
