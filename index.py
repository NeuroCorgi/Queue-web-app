from os import getenv
from uuid import uuid4
from datetime import timedelta

from flask import (
    Flask,
    render_template,
    redirect,
    jsonify
)
from flask_login.utils import login_required
from flask_socketio import (
    SocketIO,
    emit,
    join_room,
)
from flask_login import (
    LoginManager,
    current_user,
)
from flask_wtf.csrf import CSRFProtect

from data import __all_models as models
from data import db_session as db

from forms import SearchForm

app = Flask(__name__)

socket = SocketIO(app)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)

secret_key = str(uuid4())
app.config['SECRET_KEY'] = secret_key
app.config["WTF_CSRF_SECRET_KEY"] = secret_key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.config['DATABASE_NAME'] = getenv("DATABASE_URL")

db.global_init(app.config["DATABASE_NAME"])
    
import auth
app.register_blueprint(auth.blueprint)

import lessons
app.register_blueprint(lessons.blueprint)


@login_manager.user_loader
def load_user(user_id):
    session = db.create_session()
    return session.query(models.user.User).get(user_id)


@socket.on("join")
def get_queue(data):
    room = data["lesson_id"]
    join_room(room)
    session = db.create_session()
    lesson = session.query(models.lesson.Lesson).filter(models.lesson.Lesson.id == int(room)).first()
    emit("init", lesson.get_queue())


@socket.on("getin")
@login_required
def get_in(data):
    room = data["lesson_id"]
    session = db.create_session()
    node = models.queue.Node(
        user=current_user.id,
        lesson=int(room)
    )
    session.add(node)
    session.commit()
    lesson = session.query(models.lesson.Lesson).filter(models.lesson.Lesson.id == int(room)).first()
    emit("update", lesson.get_queue(), broadcast=True, to=room)


@socket.on("next")
@login_required
def get_in(data):
    room = data["lesson_id"]
    session = db.create_session()
    node = session.query(models.queue.Node).\
                   filter(models.queue.Node.lesson == int(room)).\
                   order_by(models.queue.Node.time.asc()).\
                   first()
    session.delete(node)
    session.commit()
    lesson = session.query(models.lesson.Lesson).filter(models.lesson.Lesson.id == int(room)).first()
    emit("update", lesson.get_queue(), broadcast=True, to=room)


@app.route("/", methods=["GET", "POST"])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        session = db.create_session()
        if (lessons := session.query(models.lesson.Lesson).\
            filter(models.lesson.Lesson.name.startswith(form.search.data)).all()):
            return render_template("home.html", title="Home", form=form, current_user=current_user, lessons=lessons)
        return render_template("home.html", title="Home", form=form, current_user=current_user, message="Nothing")
    return render_template("home.html", title="Home", form=form, current_user=current_user)


@app.route("/<int:id>/getin")
def getin(id):
    session = db.create_session()
    node = models.queue.Node(
        user=current_user.id,
        lesson=id
    )
    session.add(node)
    session.commit()
    return redirect(f"/{id}")


def main(*args, **kwargs):

    # app.run()
    socket.run(app, *args, **kwargs)


if __name__ == "__main__":
    app.run()
