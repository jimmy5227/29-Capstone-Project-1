from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional

class UserAddForm(FlaskForm):
    """Form for adding users"""

    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    # birthday = DateTimeField('Date of Birth', format='%m/%d/%y', validators=[DataRequired()])