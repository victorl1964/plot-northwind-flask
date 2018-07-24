#def calculate_total_renglon(row):
#    return (row['Cantidad Productos'] * row['Precio U'])
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib.ticker as ticker

def obtener_ano_semestre_trimestre(row):
    year,month,_=str(row['Date']).split('-')
    row['Year']=year
    if int(month) > 6:
        row['Semester'] = year+'-'+'02'
        if int(month) > 9:
            row['Quarter']=year+'-'+'04'
        else:
            row['Quarter']=year+'-'+'03'
    else:
        row['Semester'] = year+'-'+'01'
        if int(month) > 3:
            row['Quarter']=year+'-'+'02'
        else:
            row['Quarter']=year+'-'+'01'
    return row


def obtener_fecha_as_datetime(row):
    return (pd.to_datetime(row['Date'],format='%Y-%m-%d'))




def plot_hist(general_params, data_params):
    (fig_size1,fig_size2,fig_title,xlabel,spines,rotation,bgcolor)=general_params
    plt.figure(figsize=(fig_size1,fig_size2))

    ###PLOTTING###
    for s in data_params:
            plt.hist(s['data'],bins=s['bins'],histtype=s['histtype'],color=s['color'])
    ###SETTING FIGURE FEATURES (LABELS, SPINES, TICKS, BGCOLOR)
    plt.title(fig_title)
    plt.gca().set_ylabel("Quantity")
    plt.gca().set_xlabel(xlabel)
    plt.gca().set_facecolor(bgcolor)

    if rotation != 0:
        for item in x.get_ticklabels():
            item.set_rotation(rotation)
    for spine in spines:
        plt.gca().spines[spine].set_visible(False)
    plt.tick_params(top=False, bottom=False, left=False, right=False, labelbottom=True)


    ###BUILDING THE IMAGE BEFORE RENDERING
    image = BytesIO()
    plt.savefig(image, format='png')
    image.seek(0) # rewind to beginning of file
    png_figure = base64.b64encode(image.getvalue()).decode()
    return png_figure
"""
This function assume that more than one serie can be plotted in the same area, so
the input params which applies to all series are:

figsize1,figsize2 : Height and width of the graph
figtitle string to write at the top of the plot
indextype:  N=Numeric, S=String, D=Date (only one index for all series to plot)
xlabel = legend for X axis
ylabel = legend for Y axis
xticklabels = list of string replacements for xticklabels
spines = list of spines to be disabled
rotation = rotation angle for xtickslabels

Now, for each serie, one could have:
     data : series data
     indextype: N=Numeric, S=String, D=Date
     then substitute xticklabels
     dp_shape_color: datapoint shape and color
     legend : legend of this serie
     serie data: data for this serie
     lw: line witdh
     annotate: should the datapoints be annotated or not

     Given that, a list of dictionaries can be passed to the function, like this:
           [{},{},{},...]
     and each dictionary would be somthing like this:
            {'data':  serie1, 'legend': '...', 'datapoint': '-g', 'annotate': y}


This in an example on how to build params and call this function:


fig_size1=12
fig_size2=6
fig_title="PUNTOS DE CUENTA: Tiempo PROMEDIO por Actividad"
sindex = the index for all the series to plot
indextype = 'N'
xlabel="Actividades"
ylabel="Duración [DIAS]"
xtickslabels=(['-',
          'Intr. Solicitud (Solicitante)',
          'Rev. Solicitud (Solicitante)',
          'Validar Solicitud (Líder)',
          'Rev. Imputación (Presup.)',
          'Validar Solicitud (DE)',
          'Validad Solicitud (Presid.)',
          'Firmar Solicitud (Presid.)',
          '-'])
spines=['top','right']
rotation=45
serie_01={'data': mean_1p, 'dp_shape_color': 'o-g', 'lw':2, 'legend': 'Tiempo Promedio x Actividad ' + primer_p, 'annotate': 'f'}
#serie_02=...
#serie_03=...
general_params=(fig_size1,fig_size2,fig_title,xlabel,ylabel,xtickslabels,spines,rotation)
data_params=list([])
data_params.append(serie_01)
#data_params.append(serie_02)
#data_params.append(serie_03)
plot_lines(general_params,data_params)

"""


def plot_lines(general_params,data_params):
    (fig_size1,fig_size2,fig_title,sindex,indextype,xlabel,ylabel,spines,rotation,bgcolor)=general_params
    plt.figure(figsize=(fig_size1,fig_size2))
    xtickslabels=list([])
    ###STORING INDEX VALUES IN A TEMP AREA, BECAUSE WE WILL BE PLOTTING WITH A CONSECUTIVE Numeric
    ###INDEX FIRST
    [xtickslabels.append(sindex[i]) for i in range(len(sindex))]
    tempindex=[i for i in range(len(sindex))]

    legends=list([])
    ###PLOTTING###
    for s in data_params:
        plt.plot(tempindex, s['data'].values, s['dp_shape_color'], lw=s['lw'])
        legends.append(s['legend'])
        if s['annotate']=='y':
            for X, Y in zip(tempindex, s['data'].values):
                #0.0f is used to format a number without any decimals
                #plt.gca().annotate('{:0.2f}'.format(Y), xy=(X,Y), xytext=(-5, 5), ha='left', size=8,  textcoords='offset points')
                plt.gca().annotate('{:0.0f}'.format(Y), xy=(X,Y), xytext=(-5, 5), ha='left', size=8,  textcoords='offset points')
    ###SETTING FIGURE FEATURES (LABELS, SPINES, TICKS, BGCOLOR)
    plt.legend(legends)
    plt.title(fig_title)
    plt.gca().set_xlabel(xlabel)
    plt.gca().set_ylabel(ylabel)

    #CON ESTE CÓDIGO SE REALMENTE QUE HAY EN LAS ETIQUETAS
    #for label in plt.gca().get_xticks():
    #    print(label)

    #FIXING the x axis tickers spacing and labels
    tick_spacing = 1
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.xticks(tempindex,xtickslabels)

    x = plt.gca().xaxis
    if rotation != 0:
        for item in x.get_ticklabels():
            item.set_rotation(rotation)
    for spine in spines:
        plt.gca().spines[spine].set_visible(False)
    plt.tick_params(top=False, bottom=False, left=False, right=False, labelbottom=True)
    plt.gca().set_facecolor(bgcolor)
    ###BUILDING THE IMAGE BEFORE RENDERING###

    image = BytesIO()
    plt.savefig(image, format='png')
    image.seek(0) # rewind to beginning of file
    png_figure = base64.b64encode(image.getvalue()).decode()
    return png_figure
    #plt.yticks(np.arange(1,7,0.5));

def plot_bars(general_params,data_params):
    #REQUIRES MATPLOTLIB 2.2 TO SET EDGECOLOR AND LINEWIDTH IN BARS
    (fig_size1,fig_size2,fig_title,sindex,indextype,xlabel,ylabel,spines,rotation,bgcolor)=general_params
    xtickslabels=list([])
    [xtickslabels.append(sindex[i]) for i in range(len(sindex))]
    plt.figure(figsize=(fig_size1,fig_size2))
    tempindex=[i for i in range(len(sindex))]
    ###PLOTTING###
    legends=list([])
    for s in data_params:
        bars=plt.bar(tempindex, s['data'].values, align='center', linewidth=2, edgecolor=s['edgecolor'], color=s['color'])
        legends.append(s['legend'])
        if s['annotate']=='y':
            print("ok")
        if s['color_highest']=='y':
            max_height=get_max_height(bars)
            for bar in bars:
                if bar.get_height() == max_height:
                    bar.set_color('#700000')
    ###SETTING FIGURE FEATURES (LABELS, SPINES, TICKS, BGCOLOR)
    plt.legend(legends)
    plt.title(fig_title)
    plt.gca().set_xlabel(xlabel)
    plt.gca().set_ylabel(ylabel)
    plt.gca().set_facecolor(bgcolor)
    #FIXING the x axis tickers spacing
    tick_spacing = 1
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.xticks(tempindex,xtickslabels)
    x = plt.gca().xaxis
    if rotation != 0:
        for item in x.get_ticklabels():
            item.set_rotation(rotation)
    plt.tick_params(top=False, bottom=False, left=False, right=False, labelbottom=True)
    for spine in spines:
        plt.gca().spines[spine].set_visible(False)

    ###BUILDING THE IMAGE BEFORE RENDERING###
    image = BytesIO()
    plt.savefig(image, format='png')
    image.seek(0) # rewind to beginning of file
    png_figure = base64.b64encode(image.getvalue()).decode()
    return png_figure
    #plt.yticks(np.arange(1,7,0.5));

def plot_combined(general_params,data_params):
    #REQUIRES MATPLOTLIB 2.2 TO SET EDGECOLOR AND LINEWIDTH IN BARS
    (fig_size1,fig_size2,fig_title,sindex,indextype,xlabel,ylabel,spines,rotation,bgcolor)=general_params
    xtickslabels=list([])
    [xtickslabels.append(sindex[i]) for i in range(len(sindex))]
    plt.figure(figsize=(fig_size1,fig_size2))
    tempindex=[i for i in range(len(sindex))]

    #print("Labels are: {}".format(xtickslabels))

    legends=list([])
    ###PLOTTING
    for s in data_params:
        plt.plot(tempindex, s['data'].values, s['dp_shape_color'], lw=s['lw'])
        bars=plt.bar(tempindex, s['data'].values, align='center', linewidth=2, edgecolor=s['edgecolor'], color=s['color'])
        legends.append(s['legend'])
        if s['annotate']=='y':
            for X, Y in zip(tempindex, s['data'].values):
                plt.gca().annotate('{:0.0f}'.format(Y), xy=(X,Y), xytext=(-5, 5), ha='left', size=8,  textcoords='offset points')
        if s['color_highest']=='y':
            max_height=get_max_height(bars)
            for bar in bars:
                if bar.get_height() == max_height:
                    bar.set_color('#700000')

    ###SETTING FIGURE FEATURES (LABELS, SPINES, TICKS, BGCOLOR)
    plt.legend(legends)
    plt.title(fig_title)
    plt.gca().set_xlabel(xlabel)
    plt.gca().set_ylabel(ylabel)
    plt.gca().set_facecolor(bgcolor)
    #plt.gca().set_xticks(tempindex)

    tick_spacing = 1
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    plt.xticks(tempindex,xtickslabels)
    x = plt.gca().xaxis
    if rotation != 0:
        for item in x.get_ticklabels():
            item.set_rotation(rotation)
    for spine in spines:
        plt.gca().spines[spine].set_visible(False)
    plt.tick_params(top=False, bottom=False, left=False, right=False, labelbottom=True)


    ###BUILDING THE IMAGE BEFORE RENDERING
    image = BytesIO()
    plt.savefig(image, format='png')
    image.seek(0) # rewind to beginning of file
    png_figure = base64.b64encode(image.getvalue()).decode()
    return png_figure
    #plt.yticks(np.arange(1,7,0.5));

def get_max_height(bars):
    max_height=0
    for bar in bars:
        if bar.get_height() > max_height:
            max_height=bar.get_height()
    return max_height
