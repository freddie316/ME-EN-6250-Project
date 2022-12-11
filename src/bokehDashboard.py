#output_file-to save the layout in file, show-display the layout , output_notebook-to configure the default output state  to generate the output in jupytor notebook.
#from bokeh.io import output_file, show, output_notebook
#ColumnDataSource makes selection of the column easier and Select is used to create drop down
# from bokeh.models import ColumnDataSource, Select
#Figure objects have many glyph methods that can be used to draw vectorized graphical glyphs. example of glyphs-circle, line, scattter etc.
# from bokeh.plotting import figure
#To create intractive plot we need this to add callback method.
# from bokeh.models import CustomJS
#This is for creating layout
import os
import numpy as np
import pandas as pd
from datetime import date
from pathlib import Path
from ScrapeWebsite import scrape_country
from bokeh.layouts import column, row, gridplot
from bokeh.models import CustomJS, Dropdown, AutocompleteInput, DateRangeSlider, CheckboxGroup, ColumnDataSource, Select
from bokeh.plotting import figure, output_file, show

outputPath = Path(os.getcwd())
outputPath = outputPath.parent.absolute()
outputPath = os.path.join(outputPath, 'output\\covid-dashboard.html')
output = output_file(outputPath)

# Scraping data from WorldOMeter
site = 'WorldOMeter'

# Function for populating the data frames
def populate_dataframes(continents):
    globals()['dfMaster'] = pd.DataFrame()
    for key in continents:
        globals()['df'+key] = pd.DataFrame()
        for country in continents[key]:
            if globals()['df'+key].empty == True:
                globals()['df'+key] = scrape_country(country,site)
            else:
                df = scrape_country(country,site)
                globals()['df'+key] = pd.concat([df,globals()['df'+key]],ignore_index=True)
        if globals()['dfMaster'].empty == True:
            globals()['dfMaster'] = globals()['df'+key]
        else:
            globals()['dfMaster'] = pd.concat([globals()['dfMaster'],globals()['df'+key]],ignore_index=True)
    
continents = {'Europe':['Russia','Germany','UK'],
'NAmerica':['USA','Mexico','Canada'],
'Asia':['China','India','Indonesia'],
'SAmerica':['Brazil','Colombia','Argentina'],
'Africa':['Nigeria','Ethiopia','Egypt'],
'Oceania':['Australia','Papua New Guinea','New Zealand']}

populate_dataframes(continents)
# note, IDE marks variables created inside the function as undefined
# yet, the variables WILL be defined once the function runs.

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

# Pasted below is the code from bokehLinkedInputs to create an interactive image with dropdown box and date slider - inputs need to be modified to dataframe from this code
df_overall = dfMaster
df_overall = df_overall.sort_values(['Country', 'Date'], ascending=[True, True]) #Sorts the dataframe.

df_current = df_overall[df_overall['Country']=='USA'] #Pulls out a column showing just the USA

Overall = ColumnDataSource(df_overall) #Puts the dataframe for all of the countries into a datasource useable by Javascript
Current = ColumnDataSource(df_current) #Another DataSource that will be used for plotting

# ---- JavaScript Codes to be used
alert_code = """
//I used alerts to make sure that certain things were working. This can also be used to print variables within JavaScript
alert('A change was made')
"""

dropdown_code = """
// Code used to update the plot when the dropdown country changes.
var start = daterange.data['start_date']
var end = daterange.data['end_date']
var f = cb_obj.value
sc.data['Date'] = []
sc.data['Deaths'] = []
sc.data['Deaths per mill'] = []
sc.data['Death Rate'] = []
sc.data['Death Rate per mill'] = []
sc.data['Country'] = []

//Goes through the Overall datasource and adds to the Current datasource based on country and date selection
for(var i = 0; i <= source.get_length(); i++){
    if (source.data['Country'][i] == f && source.data['Date'][i]<=end && source.data['Date'][i]>=start){
        sc.data['Date'].push(source.data['Date'][i]);
        sc.data['Deaths'].push(source.data['Deaths'][i]);
        sc.data['Deaths per mill'].push(source.data['Deaths per mill'][i]);
        sc.data['Death Rate'].push(source.data['Death Rate'][i]);
        sc.data['Death Rate per mill'].push(source.data['Death Rate per mill'][i]);
        sc.data['Country'].push(source.data['Country'][i]);
    }
}

sc.change.emit(); //Used to make sure the change actually goes through
"""


date_code = """
//Code used to update the plot when the date slider changes. This also updates a daterange datasource so that the range is propogated to be used in dropdown_code
var f = cb_obj.value
daterange.data['start_date'] = f[0]
daterange.data['end_date'] = f[1]
daterange.change.emit();

var start = daterange.data['start_date']
var end = daterange.data['end_date']
var country = sc.data['Country'][0]

sc.data['Date'] = []
sc.data['Deaths'] = []
sc.data['Deaths per mill'] = []
sc.data['Death Rate'] = []
sc.data['Death Rate per mill'] = []

for(var i = 0; i <= source.get_length(); i++){
    if (source.data['Country'][i] == country && source.data['Date'][i]<=end && source.data['Date'][i]>=start){
        sc.data['Date'].push(source.data['Date'][i]);
        sc.data['Deaths'].push(source.data['Deaths'][i]);
        sc.data['Deaths per mill'].push(source.data['Deaths per mill'][i]);
        sc.data['Death Rate'].push(source.data['Death Rate'][i]);
        sc.data['Death Rate per mill'].push(source.data['Death Rate per mill'][i]);
    }
}

sc.change.emit();
"""
# ---- Create a dataframe from the list

valid_dates = {'start_date' : date(2022,12,7), 'end_date' : date(2022,12,9)}
valid_dates = pd.DataFrame(valid_dates, index=[0])

daterange = ColumnDataSource(valid_dates) #Date range used for plotting. 

update_dropdown = CustomJS(args = dict(source=Overall, sc=Current, daterange = daterange), code=dropdown_code) #Shows the Javascript code what to run when the dropdown is changed.
update_date = CustomJS(args = dict(source=Overall, sc=Current, daterange = daterange), code = date_code)

dropdown = Select(options = ['USA','India'], title = 'Choose Country', value = 'USA') #Initializes the dropdown with USA selected
dateslider = DateRangeSlider(title = 'Time Range', start = date(2022,12,7), end = date(2022,12,9), value =(date(2022,12,7),date(2022,12,9)), step=1) #Initializes the date slider

dropdown.js_on_change('value',update_dropdown) #Passes the dropdown value into the update_dropdown function handle
dateslider.js_on_change('value',update_date)

p = figure(x_axis_label = 'Date', y_axis_label = 'Count',x_axis_type='datetime',) #Initialize the figure
p.line(x='Date',y='Deaths',source=Current, legend_label="Deaths",line_color="blue") #source=Current links the plot to the Current datasource. Any changes done to "Current" will be automatically graphed.
p.line(x='Date',y='Death Rate',source=Current, legend_label="Death Rate",line_color="red")
p.line(x='Date',y='Deaths per mill',source=Current, legend_label="Deaths per mill",line_color="orange")
p.line(x='Date',y='Death Rate per mill',source=Current, legend_label="Death Rate per mill",line_color="purple")
p.legend.location = "top_left"
p.legend.click_policy="hide"
#p.multi_line(xs = 'Date', ys = 'Deaths', source = Current)

# TODO - change plot to be whatever we're actually using for this
display_interactive = column(dropdown,dateslider,p)

## This section puts them together
layout = column(row(display_big,display_zoomed),display_interactive)
#layout = gridplot([[display_big, display_zoomed],[display_interactive, None]])  # creating the layout
show(layout)  # displaying the layout