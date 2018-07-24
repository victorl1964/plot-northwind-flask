Basic Functional Requirements:
-----------------------------

1) An initial interface that shows some records from northwind order/orderdetails (and some other tables ...)
   , lets say 10. You might even be able to paginate those records. The implementation could consider to
   extract records from the northwind database and store them in a Pandas Dataframe. The PANDAS dataframe
   could be loaded when the application is started (config.py) . You could have a model in which an object
   for the orders/order_detail dataframe is defined, and methods to generate different plots or visualizations 


   The first implementation might be made without SQLAlchemy, just by connecting Python with Postgres directly.
   But is a good idea to use models.py and SQLAlchemy to get the data and store it in the dataframe

   This interface should generate or show different links to visualize some plots, using matplotlib


   The interface could look kind of this :

          Column 1   Column 2   Column 3 ........ Column n
          ------------------------------------------------

          xxxxxx     xxxxxxx    xxxxxxx           xxxxxxx
          xxxxxx     xxxxxxx    xxxxxxx           xxxxxxx
	  xxxxxx     xxxxxxx    xxxxxxx           xxxxxxx
          ...
          ...
          ...

          
          Visualize:
		   Visualization 1
		   Visualization 2

		   .
		   .
		   Visualization n 

    This interface could even have a form object to implement a filter x period (Select year, for example)
    ,thus alowing the user to select data from a given period of time
	
2) Several interfaces must be implemented to plot different visualizations, corresponding
                  to information like this                    

		   Orders per period 
                   Orders per vendor
                   Total money sold per product ....
                   Total money sold per period ...
		   Total money sold per vendor 
                   .
                   .
                   .
 	These interfaces should use matplotlib

        Maybe a  unique interface is enough, but different funtions will likely be needed for
	every different plot

        plots programs or functions may be implemented as generic pieces of code. For example
	You could have a function to plot serie. When the axis values are similar, you could
        plot several series in the same graph, each serie can be passed to the plotting
        function with its labels, color, line object (a dot, a dash, etc)... 

