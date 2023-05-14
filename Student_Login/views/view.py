from wtforms import Form, StringField, TextAreaField, PasswordField, validators

# Register Form Class
class RegisterForm(Form):
    studentName = StringField("Student Name", [validators.Length(min=1, max=100)])
    studentUsername = StringField('Username- Student ID number', [validators.Length(min=1, max=25)])
    email = StringField('Email', [validators.Length(min=1, max=50)])
    mobile = StringField("Mobile Number", [validators.Length(min=12, max=12)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
        ])
    confirm = PasswordField('Confirm Password')