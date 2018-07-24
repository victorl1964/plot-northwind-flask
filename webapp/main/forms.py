"""
   Forms are created as classes, with each member as an input field of
   the form
"""


from flask_wtf import FlaskForm
""" Here we specify which types of INPUT FIELDS the forms below will be able
    to implement
"""
from wtforms import SelectField, SubmitField


class SelectGraphForm(FlaskForm):
    plottype = SelectField('Select plot type : ', choices=[('line', 'Lines'), ('bar', 'Bars'), ('comb', 'Mixed')])
    submit = SubmitField('Send')
