from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired, NumberRange

EXERCISE_LEVELS = ["None", "Light", "Moderate", "Intense"]
MENSTRUAL_STATUSES = [
    "Regular cycle",
    "Irregular cycle",
    "Hormonal contraceptive",
    "Menstrual suppression",
    "Not applicable",
]


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log in")


def _number(label):
    # InputRequired (not DataRequired) so that 0 is accepted as a valid number
    return IntegerField(
        label,
        validators=[
            InputRequired(message="Enter a whole number."),
            NumberRange(min=0, message="Enter 0 or more."),
        ],
    )


def _choice(label, choices):
    return SelectField(
        label,
        choices=[("", "Select...")] + [(c, c) for c in choices],
        validators=[DataRequired(message="Choose an option.")],
    )


class HealthStatsForm(FlaskForm):
    """Used for both the Earth baseline and the space stats (same 8 fields)."""

    blood_pressure = _number("Blood Pressure (systolic, mmHg)")
    heart_rate = _number("Heart Rate (bpm)")
    exercise_level = _choice("Exercise Level", EXERCISE_LEVELS)
    water_intake = _number("Water Intake / Hydration (cups per day)")
    menstrual_status = _choice("Menstrual / Contraceptive Status", MENSTRUAL_STATUSES)
    radiation_dose = _number("Radiation Dose (mSv)")
    estrogen_level = _number("Hormone: Estrogen Level (pg/mL)")
    sleep = _number("Sleep (hours per night)")
    submit = SubmitField("Submit")

    @property
    def stat_fields(self):
        return [
            self.blood_pressure,
            self.heart_rate,
            self.exercise_level,
            self.water_intake,
            self.menstrual_status,
            self.radiation_dose,
            self.estrogen_level,
            self.sleep,
        ]
