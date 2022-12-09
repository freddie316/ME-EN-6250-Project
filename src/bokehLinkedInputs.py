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
country_data.append({'Country':'USA','Date':date(2022,12,7),'Deaths':100000,'Deaths per mill':10,'Death Rate':5,'Death Rate per mill':1})
country_data.append({'Country':'USA','Date':date(2022,12,8),'Deaths':1000,'Deaths per mill':8,'Death Rate':3,'Death Rate per mill':2})
country_data.append({'Country':'USA','Date':date(2022,12,9),'Deaths':500,'Deaths per mill':6,'Death Rate':8,'Death Rate per mill':4})
country_data.append({'Country':'India','Date':date(2022,12,7),'Deaths':500,'Deaths per mill':6,'Death Rate':8,'Death Rate per mill':4})
country_data.append({'Country':'India','Date':date(2022,12,8),'Deaths':1000,'Deaths per mill':8,'Death Rate':3,'Death Rate per mill':2})
country_data.append({'Country':'India','Date':date(2022,12,9),'Deaths':100000,'Deaths per mill':10,'Death Rate':5,'Death Rate per mill':1})

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
sc.data['Deaths'] = []
sc.data['Country'] = []

//Goes through the Overall datasource and adds to the Current datasource based on country and date selection
for(var i = 0; i <= source.get_length(); i++){
    if (source.data['Country'][i] == f && source.data['Date'][i]<=end && source.data['Date'][i]>=start){
        sc.data['Date'].push(source.data['Date'][i]);
        sc.data['Deaths'].push(source.data['Deaths'][i]);
        sc.data['Country'].push(source.data['Country'][i]);
        //alert(source.data['Deaths'][i])
        //alert(sc.data['Deaths'][i])
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


for(var i = 0; i <= source.get_length(); i++){
    if (source.data['Country'][i] == country && source.data['Date'][i]<=end && source.data['Date'][i]>=start){
        sc.data['Date'].push(source.data['Date'][i]);
        sc.data['Deaths'].push(source.data['Deaths'][i]);
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
dateslider = DateRangeSlider(title = 'Time Range', start = date(2022,12,7), end = date(2022,12,9), value =(date(2022,12,7),date(2022,12,9)), step=86400000) #Initializes the date slider

dropdown.js_on_change('value',update_dropdown) #Passes the dropdown value into the update_dropdown function handle
dateslider.js_on_change('value',update_date)

p = figure(x_axis_label = 'Date', y_axis_label = 'Deaths',x_axis_type='datetime') #Initialize the figure
p.line(x='Date',y='Deaths',source=Current) #source=Current links the plot to the Current datasource. Any changes done to "Current" will be automatically graphed.

show(column(dropdown,dateslider,p)) #Creates the bokeh image

