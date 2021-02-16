from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired
from wtforms import StringField, IntegerField, TextAreaField, SubmitField,  SelectField
from .models import Customer

class CustomerForm(FlaskForm):
    customer_ssn_id  = StringField(u"Customer SSN ID ",validators=[DataRequired(),Length(min=9,max=9)])
    customer_name = StringField("Customer Name",validators=[DataRequired(),Length(min=5,max=50)])
    customer_age = IntegerField("Age ",validators=[DataRequired(),NumberRange(min=1,max=100)])
    customer_address = TextAreaField("Address",validators=[DataRequired(),Length(max=400)])
    customer_state = SelectField("State",choices=[('UP', 'UTTAR PRADESH'), ('MP','Madhya Pradesh'),('AP','Andhra Pradesh'),('TN','Tamil Nadu'),('K','Kerala'),('M','maharashtra')])
    customer_city = SelectField("City",choices=[('H', 'Hapur'), ('M', 'morababad'),('F','faridabad'),('Hy','hyderabad')],default="Choose a State")
    submit = SubmitField("Submit")



class DeleteForm(FlaskForm):
    customer_ssn_id  = IntegerField(u"SSN ID ",validators=[DataRequired(),NumberRange(min=100000001,max=999999999)])
    customer_id = IntegerField(u"Customer ID ", validators=[DataRequired(), NumberRange(min=100000001,max=999999999)])
    customer_name = StringField("Customer Name",validators=[DataRequired(),Length(min=5,max=50)])
    customer_age = IntegerField("Age ",validators=[DataRequired(),NumberRange(min=1,max=100)])
    customer_address = TextAreaField("Address",validators=[DataRequired(),Length(max=400)])
    submit = SubmitField("Submit")




