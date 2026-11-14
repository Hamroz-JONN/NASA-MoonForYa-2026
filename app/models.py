from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    submissions = db.relationship("Submission", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    value_1 = db.Column(db.Float, nullable=False)
    value_2 = db.Column(db.Float, nullable=False)
    value_3 = db.Column(db.Float, nullable=False)
    value_4 = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def values(self):
        return [self.value_1, self.value_2, self.value_3, self.value_4]


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
