from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log in")


class SubmissionForm(FlaskForm):
    # InputRequired (not DataRequired) so that 0 is accepted as a valid number
    value_1 = FloatField("Bone Density", validators=[InputRequired(message="Enter a number.")])
    value_2 = FloatField("Radiation Level", validators=[InputRequired(message="Enter a number.")])
    value_3 = FloatField("Hormonal Measurement", validators=[InputRequired(message="Enter a number.")])
    value_4 = FloatField("Other Indicator", validators=[InputRequired(message="Enter a number.")])
    submit = SubmitField("Submit")

    @property
    def number_fields(self):
        return [self.value_1, self.value_2, self.value_3, self.value_4]
