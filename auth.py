from flask import (
    render_template,
    redirect,
    Blueprint
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)

from data import __all_models as models
from data import db_session as db

from forms import (
    RegisterForm,
    LoginForm,
)

blueprint = Blueprint('auth_api', __name__,
                      template_folder='templates/auth')


@blueprint.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db.create_session()
        if session.query(models.user.User).\
                   filter(models.user.User.saxion_id == form.saxion_id.data).first():
            return render_template('register.html', title='Sign up', current_user=current_user,
                                   form=form,
                                   message="User exists")
        user = models.user.User(
            name=form.name.data,
            saxion_id=form.saxion_id.data
        )
        session.add(user)
        session.commit()
        login_user(user, remember=True)
        return redirect('/')
    return render_template('signup.html', title='Sign up', form=form, current_user=current_user)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db.create_session()
        if (user := session.query(models.user.User).\
                            filter(models.user.User.saxion_id == form.saxion_id.data).first()):
            login_user(user, remember=True)
            return redirect("/")
        return render_template('login.html', current_user=current_user,
                               message="User does not exist",
                               form=form)
    return render_template('login.html', title='Log in', form=form, current_user=current_user)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
