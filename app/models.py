from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager

# (column name, short label, unit) for the 8 health stats, in display order
STAT_FIELDS = [
    ("blood_pressure", "Blood pressure", "mmHg"),
    ("heart_rate", "Heart rate", "bpm"),
    ("exercise_level", "Exercise level", ""),
    ("water_intake", "Water intake", "cups"),
    ("menstrual_status", "Menstrual / contraceptive status", ""),
    ("radiation_dose", "Radiation dose", "mSv"),
    ("estrogen_level", "Estrogen level", "pg/mL"),
    ("sleep", "Sleep", "h"),
]


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    earth_submissions = db.relationship("EarthSubmission", backref="user", lazy=True)
    space_submissions = db.relationship("SpaceSubmission", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class HealthStatsMixin:
    """The 8 columns shared by the earth and space submission tables."""

    id = db.Column(db.Integer, primary_key=True)
    blood_pressure = db.Column(db.Integer, nullable=False)
    heart_rate = db.Column(db.Integer, nullable=False)
    exercise_level = db.Column(db.String(50), nullable=False)
    water_intake = db.Column(db.Integer, nullable=False)
    menstrual_status = db.Column(db.String(50), nullable=False)
    radiation_dose = db.Column(db.Integer, nullable=False)
    estrogen_level = db.Column(db.Integer, nullable=False)
    sleep = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @classmethod
    def latest_for(cls, user_id):
        return db.session.scalar(
            db.select(cls)
            .filter_by(user_id=user_id)
            .order_by(cls.created_at.desc(), cls.id.desc())
            .limit(1)
        )


class EarthSubmission(HealthStatsMixin, db.Model):
    __tablename__ = "earth_submissions"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)


class SpaceSubmission(HealthStatsMixin, db.Model):
    __tablename__ = "space_submissions"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)


def match_percent(earth_value, space_value):
    """How full a comparison bar is: 100 when space equals earth, less as they differ.

    Numbers shrink in proportion to the change from the Earth value (a 25% change
    leaves the bar 75% full; a 100% or larger change empties it). Text values are
    either the same (100) or different (0).
    """
    if isinstance(earth_value, str) or isinstance(space_value, str):
        same = str(earth_value).strip().lower() == str(space_value).strip().lower()
        return 100 if same else 0
    if earth_value == space_value:
        return 100
    if earth_value == 0:
        return 0
    change = abs(space_value - earth_value) / abs(earth_value)
    return round(max(0.0, 1 - change) * 100)


def compare(earth, space):
    """One dict per stat with both values and the bar fill percentage."""
    bars = []
    for name, label, unit in STAT_FIELDS:
        e, s = getattr(earth, name), getattr(space, name)
        bars.append(
            {"label": label, "unit": unit, "earth": e, "space": s, "percent": match_percent(e, s)}
        )
    return bars


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
