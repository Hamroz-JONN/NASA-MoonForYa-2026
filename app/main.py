from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.forms import HealthStatsForm
from app.models import STAT_FIELDS, EarthSubmission, SpaceSubmission, compare

bp = Blueprint("main", __name__)


def _save(model, form):
    row = model(user_id=current_user.id)
    for name, _label, _unit in STAT_FIELDS:
        setattr(row, name, getattr(form, name).data)
    db.session.add(row)
    db.session.commit()


@bp.route("/")
def index():
    return redirect(url_for("main.dashboard"))


@bp.route("/baseline", methods=["GET", "POST"])
@login_required
def baseline():
    """Earth Baseline Stats: asked on first login, before the dashboard."""
    earth = EarthSubmission.latest_for(current_user.id)
    form = HealthStatsForm(obj=earth)
    if form.validate_on_submit():
        _save(EarthSubmission, form)
        flash("Your Earth baseline was saved.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("main/baseline.html", form=form, has_baseline=earth is not None)


@bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    earth = EarthSubmission.latest_for(current_user.id)
    if earth is None:
        return redirect(url_for("main.baseline"))

    form = HealthStatsForm()
    if form.validate_on_submit():
        _save(SpaceSubmission, form)
        flash("Your space stats were updated.", "success")
        # Redirect after POST so a page refresh doesn't resubmit
        return redirect(url_for("main.dashboard"))

    space = SpaceSubmission.latest_for(current_user.id)
    bars = compare(earth, space) if space else None
    return render_template("main/dashboard.html", form=form, space=space, bars=bars)


@bp.route("/history")
@login_required
def history():
    submissions = db.session.scalars(
        db.select(SpaceSubmission)
        .filter_by(user_id=current_user.id)
        .order_by(SpaceSubmission.created_at.desc(), SpaceSubmission.id.desc())
    ).all()
    return render_template("main/history.html", submissions=submissions, stat_fields=STAT_FIELDS)
