from flask import (
    Blueprint,
    render_template,
    redirect,
    abort,
    jsonify,
)
from flask_login import (
    current_user,
    login_required,
)
from sqlalchemy.orm import relation, session

from data import __all_models as  models
from data import db_session as db
from forms import (
    LessonForm
)

blueprint = Blueprint('jobs_view', __name__,
                      template_folder="templates/lesson")


@blueprint.route('/new', methods=['POST', 'GET'])
@login_required
def new_job():
    form = LessonForm()
    if form.validate_on_submit():
        session = db.create_session()
        lesson = models.lesson.Lesson(
            name=form.name.data,
            creator=current_user.id
        )
        session.add(lesson)
        session.commit()
        return redirect(f'/{lesson.id}')
    return render_template('new_lesson.html', title='New lesson', form=form, current_user=current_user)


@blueprint.route("/<int:id>")
def lesson(id):
    session = db.create_session()
    lesson = session.query(models.lesson.Lesson).filter(models.lesson.Lesson.id == id).first()

    if lesson:
        return render_template("lesson.html", lesson=lesson, title=lesson.name, current_user=current_user)
    return abort(404)


@blueprint.route('/<int:id>/delete')
@login_required
def delete_job(id):
    session = db.create_session()
    if (lesson := session.query(models.lesson.Lesson).\
            filter(
                models.lesson.Lesson.id == id,
                models.lesson.Lesson.creator == current_user.id
            ).first()):
        session.delete(lesson)
        session.commit()
    else:
        abort(404)
    return redirect('/')