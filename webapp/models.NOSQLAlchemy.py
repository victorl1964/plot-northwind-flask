import pandas as pd
import numpy as np
import pickle
import psycopg2 as pgsql
from webapp import helpers as hp
import datetime as dt
import time as tm
from flask import current_app

class Orders:
    def __init__(self,dbconn):
        self.orders_dataframe=None
        self.order_details_dataframe=None
        self.dbconn=dbconn

    def load_orders_only(self,query,date_from,date_to):
        cursor=self.dbconn.cursor()
        cursor.execute(query)
        #En la lista ordenes_productos quedan todas las tuplas que satisfacen el query
        ordenes = cursor.fetchall()
        ordercolumns = (
                        ['Order No.',
                         'Date',
                         'Employee',
                         'Client',
                         'Country',
                         'Vía',
                         'Shipper',
                         'Total $'
                         ]
                        )
        self.orders_dataframe = pd.DataFrame(ordenes, columns=ordercolumns)
        self.orders_dataframe=self.orders_dataframe.apply(hp.obtener_ano_semestre_trimestre, axis=1)
        self.orders_dataframe['Date']=self.orders_dataframe.apply(hp.obtener_fecha_as_datetime, axis=1)
        #return df_orders

    def load_orders_products(self,query,date_from,date_to):
        cursor=self.dbconn.cursor()
        cursor.execute(query)
        #En la lista ordenes_productos quedan todas las tuplas que satisfacen el query
        ordenes_productos  = cursor.fetchall()
        ordercolumns = (
                        ['Order No.',
                         'Date',
                         'Employee',
                         'Client',
                         'Country',
                         'Vía',
                         'Shipper',
                         'Product',
                         'Category',
                         'Unit',
                         'Price',
                         'Total $'
                         ]
                        )
        self.order_details_dataframe = pd.DataFrame(ordenes_productos, columns=ordercolumns)
        self.order_details_dataframe=self.order_details_dataframe.apply(hp.obtener_ano_semestre_trimestre, axis=1)
        self.order_details_dataframe['Date']=self.order_details_dataframe.apply(hp.obtener_fecha_as_datetime, axis=1)
        #return df_orders

    def get_orders_dataframe(self):
        return self.orders_dataframe

    def get_order_details_dataframe(self):
        return self.order_details_dataframe

    def get_orders_basic_stats(self):
        index_dict={'count': 'Count',
                    'mean': 'Average',
                    'min': 'Mínimum',
                    '25%': 'Perc. 25',
                    '50%': 'Perc. 50',
                    '75%': 'Perc. 75',
                    'max': 'Máximum'}

        #Changing stats column names
        orders_stats_s=self.orders_dataframe.describe()['Total $'].rename(index_dict)
        orders_stats_s=orders_stats_s.drop(labels=['std'])
        return(pd.DataFrame(orders_stats_s))

    def get_money_distrib(self):
        fig_size1=5
        fig_size2=4
        fig_title="Order Amount Histogram"
        xlabel="Order Total [$]"
        spines=['top','bottom','left','right']
        rotation=0
        bgcolor="#8cb1cf"
        serie_01={'data':self.orders_dataframe['Total $'],
                  'bins':12,
                  'histtype':'step',
                  'color':'red'
                 }
        general_params=(fig_size1,
                        fig_size2,
                        fig_title,
                        xlabel,
                        spines,
                        rotation,
                        bgcolor)
        data_params=list([])
        data_params.append(serie_01)
        png_figure=hp.plot_hist(general_params, data_params)
        return png_figure

    def get_orders_units_info(self,plottype,group_arg):
        if group_arg == 'quarter':
            orders=self.orders_dataframe.groupby('Quarter').size()
        elif group_arg == 'year':
            orders=self.orders_dataframe.groupby('Year').size()
        elif group_arg == 'month':
            orders_aux=self.orders_dataframe
            max_date=orders_aux['Date'].max()
            """Here we take the max_date to the last day of the previous month"""
            max_date-= dt.timedelta(days = max_date.day)
            """Here we compute the min_date as max_date minus a year"""
            min_date=max_date - dt.timedelta(days = 365)
            """Here we select orders in that date range"""
            orders_aux=orders_aux[(orders_aux['Date'] > min_date)  & (orders_aux['Date'] <= max_date) ]
            orders_aux.set_index('Date', inplace=True)
            #orders=orders_aux.groupby([(orders_aux.index.year),(orders_aux.index.month)])['Total Vendido'].sum()
            orders=orders_aux.groupby([(orders_aux.index.year),(orders_aux.index.month)]).size()
        elif group_arg == 'employee':
            orders=self.orders_dataframe.groupby('Employee').size().sort_values(ascending=False)
        elif group_arg == 'country':
            orders=self.orders_dataframe.groupby('Country').size().sort_values(ascending=False)
        fig_size1=8
        fig_size2=6
        fig_title="Orders by " + current_app.config['GROUP_ARGS'][group_arg]
        indextype='N'
        xlabel=current_app.config['GROUP_ARGS'][group_arg]
        ylabel="Quantity"
        spines=['top','bottom','left','right']
        rotation=90
        bgcolor="#8cb1cf"
        serie_01={'data': orders,
                  'dp_shape_color': 'o-g',
                  'lw':1,
                  'legend':'Orders',
                  'edgecolor': '#60A0D0',
                  'color': '#FFFFFF',
                  'annotate': 'y',
                  'color_highest': 'y',
                  'color_shortest': 'y'}
        general_params=(fig_size1,
                        fig_size2,
                        fig_title,
                        orders.index,
                        indextype,
                        xlabel,
                        ylabel,
                        spines,
                        rotation,
                        bgcolor)
        data_params=list([])
        data_params.append(serie_01)

        if plottype=='line':
            png_figure=hp.plot_lines(general_params,data_params)
        elif plottype=='bar':
            png_figure=hp.plot_bars(general_params,data_params)
        else:
            #data_params[0]['dp_shape_color']='o-r'
            png_figure=hp.plot_combined(general_params,data_params)

        orders=pd.DataFrame(orders).rename(columns={0: 'Quantity'})
        return  orders,png_figure

    def get_products_units_info(self,plottype):
        products=self.order_details_dataframe.groupby('Product').size().sort_values(ascending=False)

        fig_size1=8
        fig_size2=6
        fig_title="Units Sold by PRODUCT (top 20)"
        indextype='S'
        xlabel="PRODUCT"
        ylabel="Units"
        spines=['top','bottom','left','right']
        rotation=90
        bgcolor="#8cb1cf"
        serie_01={'data': products.head(20),
                  'dp_shape_color': '-g',
                  'lw':1,
                  'legend':'Product Units',
                  'edgecolor': '#60A0D0',
                  'color': '#FFFFFF',
                  'annotate': 'y',
                  'color_highest': 'y',
                  'color_shortest': 'y'}
        general_params=(fig_size1,
                        fig_size2,
                        fig_title,
                        products.index[0:20],
                        indextype,
                        xlabel,
                        ylabel,
                        spines,
                        rotation,
                        bgcolor)
        data_params=list([])
        data_params.append(serie_01)

        if plottype=='line':
            png_figure=hp.plot_lines(general_params,data_params)
        elif plottype=='bar':
            png_figure=hp.plot_bars(general_params,data_params)
        else:
            #data_params[0]['dp_shape_color']='o-r'
            png_figure=hp.plot_combined(general_params,data_params)

        products=pd.DataFrame(products).rename(columns={0: 'Units Sold'})
        return  products.head(20),png_figure


    def get_orders_revenues_info(self,plottype,group_arg):
        if group_arg == 'quarter':
            revenues=self.orders_dataframe.groupby('Quarter')['Total $'].sum()
        elif group_arg == 'year':
            revenues=self.orders_dataframe.groupby('Year')['Total $'].sum()
        elif group_arg == 'month':
            orders_aux=self.orders_dataframe
            max_date=orders_aux['Date'].max()
            """Here we take the max_date to the last day of the previous month"""
            max_date-= dt.timedelta(days = max_date.day)
            """Here we compute the min_date as max_date minus a year"""
            min_date=max_date - dt.timedelta(days = 365)
            """Here we select orders in that date range"""
            orders_aux=orders_aux[(orders_aux['Date'] > min_date)  & (orders_aux['Date'] <= max_date) ]
            orders_aux.set_index('Date', inplace=True)
            revenues=orders_aux.groupby([(orders_aux.index.year),(orders_aux.index.month)])['Total $'].sum()
        elif group_arg == 'employee':
            revenues=self.orders_dataframe.groupby('Employee')['Total $'].sum().sort_values(ascending=False)
        elif group_arg == 'country':
            revenues=self.orders_dataframe.groupby('Country')['Total $'].sum().sort_values(ascending=False)
        fig_size1=8
        fig_size2=6
        fig_title="Total Sold by " + current_app.config['GROUP_ARGS'][group_arg]
        indextype='S'
        xlabel=current_app.config['GROUP_ARGS'][group_arg]
        ylabel="Total Sold [$]"
        spines=['top','bottom','left','right']
        rotation=90
        bgcolor="#8cb1cf"
        serie_01={'data': revenues,
                  'dp_shape_color': 'o-g',
                  'lw':1,
                  'legend': 'Order Revenues',
                  'edgecolor': '#60A0D0',
                  'color': '#FFFFFF',
                  'annotate': 'y',
                  'color_highest': 'y',
                  'color_shortest': 'y'}
        general_params=(fig_size1,
                        fig_size2,
                        fig_title,
                        revenues.index,
                        indextype,
                        xlabel,
                        ylabel,
                        spines,
                        rotation,
                        bgcolor)
        data_params=list([])
        data_params.append(serie_01)

        if plottype=='line':
            png_figure=hp.plot_lines(general_params,data_params)
        elif plottype=='bar':
            png_figure=hp.plot_bars(general_params,data_params)
        else:
            #data_params[0]['dp_shape_color']='o-r'
            png_figure=hp.plot_combined(general_params,data_params)

        revenues=pd.DataFrame(revenues).rename(columns={0: 'Total Sold'})
        return  revenues,png_figure

    def get_products_revenues_info(self,plottype):
        revenues=self.order_details_dataframe.groupby('Product')['Total $'].sum().sort_values(ascending=False)

        fig_size1=8
        fig_size2=6
        fig_title="Total Sold by PRODUCT (top 20)"
        indextype='S'
        xlabel="PRODUCT"
        ylabel="Total Sold [$]"
        spines=['top','bottom','left','right']
        rotation=90
        bgcolor="#8cb1cf"
        serie_01={'data': revenues.head(20),
                  'dp_shape_color': '-g',
                  'lw':1,
                  'legend':'Product Revenues',
                  'edgecolor': '#60A0D0',
                  'color': '#FFFFFF',
                  'annotate': 'f',
                  'color_highest': 'y',
                  'color_shortest': 'y'}
        general_params=(fig_size1,
                        fig_size2,
                        fig_title,
                        revenues.index[0:20],
                        indextype,
                        xlabel,
                        ylabel,
                        spines,
                        rotation,
                        bgcolor)
        data_params=list([])
        data_params.append(serie_01)

        if plottype=='line':
            png_figure=hp.plot_lines(general_params,data_params)
        elif plottype=='bar':
            png_figure=hp.plot_bars(general_params,data_params)
        else:
            #data_params[0]['dp_shape_color']='o-r'
            png_figure=hp.plot_combined(general_params,data_params)

        revenues=pd.DataFrame(revenues).rename(columns={0: 'Total Sold'})
        return  revenues.head(20),png_figure

    © 2018 GitHub, Inc.
    Terms
    Privacy
    Security
    Status
    Help

    Contact GitHub
    API
    Training
    Shop
    Blog
    About
