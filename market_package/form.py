from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField,DateField
from wtforms.validators import Length,EqualTo, Email, DataRequired,ValidationError
from market_package.models import User

class RegisterForm(FlaskForm):
    username = StringField(label='User Name:',validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label='Email:',validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

    def validate_username(self,input_username):
        user = User.query.filter_by(username=input_username.data).first()
        if user:
            print('detecting user in db')
            raise ValidationError('This username is existed. Go to Login page or change to a new username')

    def validate_email_address(self,input_email):
        email = User.query.filter_by(email_address=input_email.data).first()
        if email:
            raise ValidationError('The email has been registered, go to Login page or change to a new email address')

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField('Purchase')

class SellItemForm(FlaskForm):
    submit = SubmitField('Sell')