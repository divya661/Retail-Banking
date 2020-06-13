from flask_wtf import Form
from wtforms.validators import DataRequired, Length,ValidationError
from wtforms import StringField, IntegerField, TextAreaField, SubmitField,  SelectField
from .models import Customer
from .exceptions import Invalid_SSN_Id

class CustomerForm(Form):
    customer_ssn_id  = IntegerField(u"Candidate SSN ID ",validators=[DataRequired(),Length(min=9,max=9)])
    customer_name = StringField("Candidate Name",validators=[DataRequired(),Length(min=5,max=50)])
    customer_age = IntegerField("Age ",validators=[DataRequired(),Length(max=3)])
    customer_address = TextAreaField("Address",validators=[DataRequired(),Length(max=400)])
    customer_state = SelectField("State",choices=[('UP', 'UTTAR PRADESH'), ('MP','Madhya Pradesh'),('AP','Andhra Pradesh'),('TN','Tamil Nadu'),('K','Kerala'),('M','maharashtra')])
    customer_city = SelectField("City",choices=[('H', 'Hapur'), ('M', 'morababad'),('F','faridabad'),('Hy','hyderabad')])
    submit = SubmitField("Submit")

 #   def validate_ssn_id(self, customer_ssn_id):
 #       ssn_id = Customer.query.filter_by(customer_ssn_id=customer_ssn_id).first()
 #       if ssn_id:
 #           raise ValidationError("The customer account with the SSN ID entered already exists")






