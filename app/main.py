from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.forms import SubmissionForm
from app.models import Submission

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return redirect(url_for("main.dashboard"))


@bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = SubmissionForm()
    if form.validate_on_submit():
        submission = Submission(
            user_id=current_user.id,
            value_1=form.value_1.data,
            value_2=form.value_2.data,
            value_3=form.value_3.data,
            value_4=form.value_4.data,
        )
        db.session.add(submission)
        db.session.commit()
        flash("Your health information was updated.", "success")
        # Redirect after POST so a page refresh doesn't resubmit
        return redirect(url_for("main.dashboard"))

    latest = db.session.scalar(
        db.select(Submission)
        .filter_by(user_id=current_user.id)
        .order_by(Submission.created_at.desc())
        .limit(1)
    )
    return render_template("main/dashboard.html", form=form, latest=latest)


@bp.route("/history")
@login_required
def history():
    submissions = db.session.scalars(
        db.select(Submission)
        .filter_by(user_id=current_user.id)
        .order_by(Submission.created_at.desc())
    ).all()
    return render_template("main/history.html", submissions=submissions)
