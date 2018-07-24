# plot-northwind
Matplotlib visualizations of the famous northwind database

This project is intended to put in practice some PYTHON/FLASK/PANDAS/MATPLOTLIB knowledge to explore the famous northwind database.


Techinical requirements are
  
  General 
  
  - PostgreSQL
  - Python 3.5
  - python3-psycopg2 (for python postgres integration)
  
  Python Plotting and DataScience libs
  
  - Matplotlib 2.2
  - Pandas
  
  Python Flask Framework
 
  Flask packages
   
   -pip install flask (flask core)
   -pip install flask-wtf (for flask forms)
   -pip install flask-mail (for e-mail management)
   -pip install flask-bootstrap (for including bootstrap CSS styles in web interfaces)
   -pip install requests (for making http requests to web services)


Initial requirements are:

- Create a PANDAS Dataframe from the NORTHWIND DATABASE
- Display some rows or records in the home page, allowing pagination
- Show some basic statistics
- Group the information by different arguments like employee, country, period, product
- Show some visualizations (lines, bars, etc).

Visualizations functions should be created so that the calling program can specify features like
spines (on/off), points labeling(on of), labels, legends, labels, xticks, background color, and the like

As the main purpose of this project is the exploration of some Python packages or libraries commonly used in
the DataScience world, and their integration to web applications, some better practices were not introduced yet,
So you won't see in this version:

- SQLAlchemy. NO ORM is being used in this release. Dataframe are created and populated in config.py, using raw queries
  against PostgreSQL
 
 -No automatic translation. Web interfaces, messages, labels, and the like, are in English (my modest English)
 
 -You won't likely see a good Object Oriented Design. Classes were designed on the fly, as ideas came to my mind,
  so a better OOD is probably needed
  
 -No JavaScript, or Ajax functionalities
 
 -Plotting functions for bars and lines can cantain many common lines of code, which mean a general plotting function
  can be designed and coded
  
 -Plotting pararameters could be specified by the user in a form, for example, legends, titles, xticks rotations, colors,
  annotating points in lines, etc. In the main time, they are passed as argument from the model to the helpers functions
  


  
  



