# ME-EN-6250-Project - A Covid-19 dashboard
Python Project for Object Oriented Programming  
Project Info: https://utah.instructure.com/courses/821474/pages/project-covid-dashboard

### Team Members:  
Freddie Rice  
Tanner Short  
Brandon Baum



### Preliminary Installation Instructions
Python and the following libraries are necessary to run ScrapeWebsite.py. Python can be installed from https://www.python.org/ or from any distribution like Anaconda.
There are several ways to install these, but we have included installation commands for pip and conda.  

Library Dependencies:
1. os and pathlib  
	- Included by default  
2. requests  
	- pip: python -m pip install requests  
	- conda: conda install requests  
3. pandas  
	- pip: python -m pip install pandas  
	- conda: conda install pandas  
4. BeautifulSoup  
	- pip: python -m pip install beautifulsoup4  
	- conda: conda install BeautifulSoup4  
5. Bokeh
	- pip: python -m pip install bokeh
	- conda: conda install bokeh
6. Selenium
	- pip: python -m pip install selenium
	- conda: conda install selenium
7. Webdriver Manager
	- pip: python -m pip install webdriver-manager
	- conda: Unavailable through conda as of writing. Use pip method.
8. Tabulate
	- pip: python -m pip install tabulate
	- conda: conda install tabulate
	
### Downloading and Running the Board  
After installing the above dependencies, you should now be ready to run the dashboard  
First, a forewarning. This was coded on windows, so there could be unexpected bugs if attempting to run this on Mac OS.  
Now, to download the zip of the files, click on the green code<> button at the top of the repository, and click the download zip button at the bottom of the drop down menu.  
To run the dashboard, first unzip the file you downloaded, then double click the start.bat. A terminal window will open, and you'll be prompted to input your desired country and website choice, then the program will display the requested data in table form after retrieving it.
