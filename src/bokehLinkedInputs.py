from bokeh.plotting import figure, show
from bokeh.models import Dropdown, Select
from datetime import date
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import TapTool, CustomJS, ColumnDataSource, Slider, DateRangeSlider
from bokeh.io import output_notebook
from bokeh.layouts import column
import os
from pathlib import Path
import warnings

## TODO Import JSON file as dictionary or pandas.DataFrame with columns for Country, Date, Deaths, Deaths per mill, Death Rate per mill, and possibly Continent

# --- This is just a filler to create a dictionary. We will want to use the actual JSON file.
country_data = []
country_data.append({'Country':'USA','Date':date(2022,12,7),'Total Deaths':100000,'Deaths/1M pop':10,'New Deaths':5,'New Deaths/1M pop':1})
country_data.append({'Country':'USA','Date':date(2022,12,8),'Total Deaths':1000,'Deaths/1M pop':8,'New Deaths':3,'New Deaths/1M pop':2})
country_data.append({'Country':'USA','Date':date(2022,12,9),'Total Deaths':500,'Deaths/1M pop':6,'New Deaths':8,'New Deaths/1M pop':4})
country_data.append({'Country':'India','Date':date(2022,12,7),'Total Deaths':500,'Deaths/1M pop':6,'New Deaths':8,'New Deaths/1M pop':4})
country_data.append({'Country':'India','Date':date(2022,12,8),'Total Deaths':1000,'Deaths/1M pop':8,'New Deaths':3,'New Deaths/1M pop':2})
country_data.append({'Country':'India','Date':date(2022,12,9),'Total Deaths':100000,'Deaths/1M pop':10,'New Deaths':5,'New Deaths/1M pop':1})

# ---- Create a dataframe from the list
df_overall = pd.DataFrame(country_data)
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
#p.line(x='Date',y='Total Deaths',source=Current, legend_label="Deaths",line_color="blue") #source=Current links the plot to the Current datasource. Any changes done to "Current" will be automatically graphed.
p.line(x='Date',y='New Deaths',source=Current, legend_label="Death Rate",line_color="red")
p.line(x='Date',y='Deaths/1M pop',source=Current, legend_label="Deaths per mill",line_color="orange")
p.line(x='Date',y='New Deaths/1M pop',source=Current, legend_label="Death Rate per mill",line_color="purple")
p.legend.location = "top_left"
p.legend.click_policy="hide"
#p.multi_line(xs = 'Date', ys = 'Total Deaths', source = Current)
show(column(dropdown,dateslider,p)) #Creates the bokeh image

