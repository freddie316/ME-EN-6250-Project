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
from datetime import date, datetime
from pathlib import Path
from ScrapeWebsite import scrape_country
from bokeh.layouts import column, row, gridplot
from bokeh.models import CustomJS, Dropdown, AutocompleteInput, DateRangeSlider, CheckboxGroup, ColumnDataSource, Select, DataTable, TableColumn
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

countries = []
for i in continents.keys():
    for j in continents[i]:
        countries.append(j)

populate_dataframes(continents)
# note, IDE marks variables created inside the function as undefined
# yet, the variables WILL be defined once the function runs.
df_overall = dfMaster
df_overall['Date'] = pd.to_datetime(df_overall['Date'])
df_overall = df_overall.sort_values(['Country','Date'], ascending=[True, True]) #Sorts the dataframe.

df_current = df_overall[df_overall['Country'] =='USA'] #Pulls out a column showing just the USA (default country plot)

Overall = ColumnDataSource(df_overall) #Puts the dataframe for all of the countries into a datasource useable by Javascript
Current = ColumnDataSource(df_current) #Another DataSource that will be used for plotting

continent_dfs = [dfNAmerica, dfAsia, dfSAmerica, dfAfrica, dfOceania, dfEurope]

for i in range(0,len(continent_dfs)):
    current_date = continent_dfs[i]['Date'].max()
    continent_dfs[i] = continent_dfs[i][continent_dfs[i]['Date']==current_date]
    #continent = continent[continent['Date']==current_date]


NAmerica = ColumnDataSource(continent_dfs[0])
Asia = ColumnDataSource(continent_dfs[1])
SAmerica = ColumnDataSource(continent_dfs[2])
Africa = ColumnDataSource(continent_dfs[3])
Oceania = ColumnDataSource(continent_dfs[4])
Europe = ColumnDataSource(continent_dfs[5])

current_continent = ColumnDataSource(continent_dfs[0])

columns = [
    TableColumn(field='Country', title='Country'),
    TableColumn(field='Date', title='Date'),
    TableColumn(field='Total Deaths', title='Total Deaths'),
    TableColumn(field='New Deaths', title='New Deaths'),
    TableColumn(field='Deaths/1M pop', title='Deaths/1M pop'),
    TableColumn(field='New Deaths/1M pop', title='New Deaths/1M pop')
    ]


zoomed_table = DataTable(source=current_continent, columns = columns)


#zoom_fig = figure(title = 'Stats by Continent', )


# TODO - The plot is used in every section, change so each display has its own figures
plot = figure(title = "Big Picture Deaths per Million People Today", x_axis_label='Country', y_axis_label='Count', x_range = df_overall[df_overall['Country']==df_overall['Country'].max()]['Deaths/1M pop'])
x = countries
y = df_overall[df_overall['Date']==df_overall['Date'].max()]['Deaths/1M pop']
plot.vbar(x,y)
# TODO - create the big display plot
display_big = plot

# TODO - update continent-list.txt to include valid continents and countries
with open('continent-list.txt') as continent_list:
    data = continent_list.read()
    valid_continents = data.split('\n')

# TODO - add functionality to Dropdown menu to update plots
zoomed_continents = Select(title = "Continent Select", options = valid_continents, value = 'North America')


continent_code = """
var continent = cb_obj.value
alert(continent);
switch(continent) {
    case 'Africa':
        curr.data = Africa.data;
        break;
    case 'Asia':
        curr.data = Asia.data;
        break;
    case 'Europe':
        curr.data = Europe.data;
        break;
    case 'North America':
        curr.data = NAmerica.data;
        break;
    case 'South America':
        curr.data = SAmerica.data;
        break;
    case 'Oceania':
        curr.data = Oceania.data;
        break;
    default:
        curr.data = curr.data;  
}

curr.change.emit();
"""

continent_select = CustomJS(args = dict(curr=current_continent, NAmerica=NAmerica, Asia = Asia,SAmerica=SAmerica,Africa=Africa,Oceania=Oceania, Europe=Europe), code = continent_code)
zoomed_continents.js_on_change('value', continent_select)

display_zoomed = column(zoomed_continents, zoomed_table)

# TODO - change to unique country-list.txt file with just the countries we scraped
with open('country-list-WOM.txt') as country_list:
    data = country_list.read()
    valid_countries = data.split('\n')

# TODO - add JS functions to each of these widgets

# Pasted below is the code from bokehLinkedInputs to create an interactive image with dropdown box and date slider - inputs need to be modified to dataframe from this code

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
sc.data['Total Deaths'] = []
sc.data['Deaths/1M pop'] = []
sc.data['New Deaths'] = []
sc.data['New Deaths/1M pop'] = []
sc.data['Country'] = []

//Goes through the Overall datasource and adds to the Current datasource based on country and date selection
for(var i = 0; i <= source.get_length(); i++){
    if (source.data['Country'][i] == f && source.data['Date'][i]<=end && source.data['Date'][i]>=start){
        sc.data['Date'].push(source.data['Date'][i]);
        sc.data['Total Deaths'].push(source.data['Total Deaths'][i]);
        sc.data['Deaths/1M pop'].push(source.data['Deaths/1M pop'][i]);
        sc.data['New Deaths'].push(source.data['New Deaths'][i]);
        sc.data['New Deaths/1M pop'].push(source.data['New Deaths/1M pop'][i]);
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
sc.data['Total Deaths'] = []
sc.data['Deaths/1M pop'] = []
sc.data['New Deaths'] = []
sc.data['New Deaths/1M pop'] = []

for(var i = 0; i <= source.get_length(); i++){
    if (source.data['Country'][i] == country && source.data['Date'][i]<=end && source.data['Date'][i]>=start){
        sc.data['Date'].push(source.data['Date'][i]);
        sc.data['Total Deaths'].push(source.data['Total Deaths'][i]);
        sc.data['Deaths/1M pop'].push(source.data['Deaths/1M pop'][i]);
        sc.data['New Deaths'].push(source.data['New Deaths'][i]);
        sc.data['New Deaths/1M pop'].push(source.data['New Deaths/1M pop'][i]);
    }
}

sc.change.emit();
"""
# ---- Create a dataframe from the list
valid_dates = {'start_date' : df_overall['Date'].min(), 'end_date' : df_overall['Date'].max()}
valid_dates = pd.DataFrame(valid_dates, index=[0])

daterange = ColumnDataSource(valid_dates) #Date range used for plotting. 

update_dropdown = CustomJS(args = dict(source=Overall, sc=Current, daterange = daterange), code=dropdown_code) #Shows the Javascript code what to run when the dropdown is changed.
update_date = CustomJS(args = dict(source=Overall, sc=Current, daterange = daterange), code = date_code)

dropdown = Select(options = countries, title = 'Choose Country', value = 'USA') #Initializes the dropdown with USA selected
dateslider = DateRangeSlider(title = 'Time Range', start = valid_dates['start_date'][0], end = valid_dates['end_date'][0], value =(valid_dates['start_date'][0],valid_dates['end_date'][0]), step=1) #Initializes the date slider

dropdown.js_on_change('value',update_dropdown) #Passes the dropdown value into the update_dropdown function handle
dateslider.js_on_change('value',update_date)

p1 = figure(title = "Total Deaths", x_axis_label = 'Date', y_axis_label = 'Total Deaths',x_axis_type='datetime',) #Initialize the figure
p1.line(x='Date',y='Total Deaths',source=Current, line_color="blue") #source=Current links the plot to the Current datasource. Any changes done to "Current" will be automatically graphed.
p2 = figure(title = "New Deaths", x_axis_label = 'Date', y_axis_label = 'New Deaths',x_axis_type='datetime',) #Initialize the figure
p2.line(x='Date',y='New Deaths',source=Current, line_color="red")
p3 = figure(title = "Deaths per Million people", x_axis_label = 'Date', y_axis_label = 'Deaths/1M pop',x_axis_type='datetime',) #Initialize the figure
p3.line(x='Date',y='Deaths/1M pop',source=Current, line_color="orange")
p4 = figure(title = "New Deaths per Million people", x_axis_label = 'Date', y_axis_label = 'New Deaths/1M pop',x_axis_type='datetime',) #Initialize the figure
p4.line(x='Date',y='New Deaths/1M pop',source=Current, line_color="purple")
#p.legend.location = "top_left"
#p.legend.click_policy="hide"
#p.multi_line(xs = 'Date', ys = 'Total Deaths', source = Current)
p = gridplot([[p1, p2],[p3, p4]])
# TODO - change plot to be whatever we're actually using for this
display_interactive = column(dropdown,dateslider,p)

## This section puts them together
layout = column(row(display_big,display_zoomed),display_interactive)
#layout = gridplot([[display_big, display_zoomed],[display_interactive, None]])  # creating the layout
show(layout)  # displaying the layout