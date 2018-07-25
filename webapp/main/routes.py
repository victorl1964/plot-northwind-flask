from webapp.main import bp
from webapp.models import OrderDfs
from datetime import datetime
from io import BytesIO
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import psycopg2 as pgsql

from io import BytesIO
import base64
from flask import render_template,flash,redirect,url_for,request, current_app, jsonify

from webapp.main.forms import SelectGraphForm

@bp.route('/',methods=['GET', 'POST'])
@bp.route('/index',methods=['GET', 'POST'])
def index():

    start = request.args.get('start', 0, type=int)
    """Here we get a reference to the orders object which was created in config.py"""
    orders=current_app.config['ORDERS']
    """ """
    orders_df=orders.get_orders_dataframe()
    orders_stats_df=orders.get_orders_basic_stats()
    stats=orders_stats_df.to_html(header=False, border=0)
    result="Dataframe was loaded OK"
    #flash('Registro de Ordenes de Compra')
    data=orders_df[start:start + current_app.config['ORDERS_PER_PAGE']].to_html(border=0,index=False)
    image=orders.get_money_distrib()
    next_url = url_for('main.index', start=start+current_app.config['ORDERS_PER_PAGE'])
    prev_url = url_for('main.index', start=start-current_app.config['ORDERS_PER_PAGE']) if start > 0 else None

    return render_template('index.html',
                            title='Orders',
                            data=data,
                            stats=stats,
                            image=image,
                            next_url=next_url,
                            prev_url=prev_url
                            )


"""WITH PARAMETERS PASSED FROM base.html, the URL is built.
"""
@bp.route('/<group_arg>/<reporttype>',methods=['GET', 'POST'])
def get_orders_info(group_arg,reporttype):

    """
    print(request.method)
    print(request.url)

    When request.method=POST, the post action is made over the same URL, which means we will have the 'periodtype' value
    available, along with the selected type of graph
    """
    default_g_type='line'
    form=SelectGraphForm()
    if form.validate_on_submit():
        default_g_type=form.plottype.data


    orders=current_app.config['ORDERS']
    orders_df=orders.get_orders_dataframe()
    if reporttype == "orders":
        (data,image)=orders.get_orders_units_info(default_g_type,group_arg)
    else:
        (data,image)=orders.get_orders_revenues_info(default_g_type,group_arg)
    result="Dataframe was loaded OK"
    #flash('Registro de Ordenes de Compra')
    return render_template('plots.html',
                            form=form,
                            title=reporttype + ' x ' + group_arg,
                            data=data.to_html(),
                            image=image,
                            width=800)


@bp.route('/products/<reporttype>',methods=['GET', 'POST'])
def get_products_info(reporttype):

    """
    print(request.method)
    print(request.url)

    When request.method=POST, the post action is made over the same URL, which means we will have the 'periodtype' value
    available, along with the selected type of graph
    """
    default_g_type='line'
    form=SelectGraphForm()
    if form.validate_on_submit():
        default_g_type=form.plottype.data


    orders=current_app.config['ORDERS']
    orders_products_df=orders.get_order_details_dataframe()
    if reporttype == "units":
            (data,image)=orders.get_products_units_info(default_g_type)
    else:
            (data,image)=orders.get_products_revenues_info(default_g_type)
    result="Dataframe was loaded OK"
    #flash('Registro de Ordenes de Compra')
    return render_template('plots.html',
                            form=form,
                            title=reporttype,
                            data=data.to_html(),
                            image=image,
                            width=800)



@bp.route('/reload',methods=['GET'])
def reload():
    """Here we reload the orders object in config.py, to refresh data"""


    orders=OrderDfs()
    orders.load_orders_only(current_app.config['DB'],None,None)
    orders.load_orders_products(current_app.config['DB'],None,None)
    return redirect(url_for('main.index')) 




""" This function is just for testing image rendering to flask's views """
@bp.route('/plot',methods=['GET', 'POST'])
def build_plot():

    plt.figure(figsize=(12,6))
    img = BytesIO()

    y = [1,2,3,4,5]
    x = [0,2,1,3,4]
    plt.plot(x,y)
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)
