from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    IntegerField,
    DateField,
)


class LoginForm(FlaskForm):
    saxion_id = StringField("saxion id", validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):

    name = StringField("name", validators=[DataRequired()])
    saxion_id = StringField("saxion id", validators=[DataRequired()])

    submit = SubmitField('Sign up')


class SearchForm(FlaskForm):

    search = StringField("search", validators=[DataRequired()])

    submit = SubmitField("Search")


class LessonForm(FlaskForm):

    name = StringField('Lesson name', validators=[DataRequired()])

    submit = SubmitField("Submit")
