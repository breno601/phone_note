from flask import Flask, flash, redirect, render_template, request, session, abort, url_for, g, make_response
from flask.ext.login import login_user, logout_user, current_user, login_required

from lib.pdf import create_pdf
from lib.email import send_email
from models import User, create_user, confirm_user, update_password
from models import Note, create_note, delete_note, update_note
from app import app, login_manager, ts


@login_manager.user_loader
def load_user(id):

    return User.query.get(int(id))


@app.before_request
def before_request():

    g.user = current_user


@app.route('/')
def home():

    if current_user.is_authenticated():
        return redirect(url_for('notes'))
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():

    username = str(request.form['username'])
    password = str(request.form['password'])

    user = User.query.filter(User.username == username).first()

    if user and user.email_confirmed and user.password == password:
        login_user(user)
        return redirect(url_for('notes'))
    else:
        flash('Wrong credentials or account email not confirmed', 'error')
        return redirect(url_for('home'))


@app.route('/logout')
def logout():

    logout_user()
    return home()


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('addUser.html')

    name = request.form.get('name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    existentUser = User.query.filter((User.username == username) | (User.email == email)).first()

    if not existentUser:
        user = create_user(name, email, username, password)

        token = ts.dumps(user.email, salt='email-confirm-key')

        confirm_url = url_for(
            'confirm_email',
            token=token,
            _external=True)

        return render_template(
            'activate.html',
            confirm_url=confirm_url)
    else:
        flash('User credentials already exists')
        return redirect(url_for('register'))


@app.route('/confirm_email/<token>')
def confirm_email(token):

    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    user = confirm_user(email)

    if user.email_confirmed:
        flash('User created successfully!')
        return home()
    else:
        flash('User invalid confirmation token!')


@app.route('/notes/', defaults={'page': 1})
@app.route('/notes/page/<int:page>')
@login_required
def notes(page=1):

    per_page = 10
    notes = Note.query.filter_by(user_id=g.user.id).order_by(Note.call_date.desc()).paginate(page, per_page, False).items
    tmpl_name = 'index.html' if page == 1 else 'notes.html'
    return render_template(tmpl_name, notes=notes, page=page)


@app.route('/note', methods=['GET', 'POST'])
@login_required
def note():

    if request.method == 'GET':
        return render_template('addNote.html')

    name = request.form.get('name')
    phone_number = request.form.get('phone')
    note = request.form.get('note')

    note = create_note(name, phone_number, note, g.user)
    flash('Note created!')
    return redirect(url_for('notes'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):

    note = Note.query.filter_by(id=id).first()

    if request.method == 'GET':
        return render_template('editNote.html', note=note)

    name = request.form.get('name')
    phone_number = request.form.get('phone')
    note = request.form.get('note')

    note = update_note(id, name, phone_number, note)
    flash('Note edited!')
    return redirect(url_for('notes'))


@app.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):

    delete_note(id)
    flash('Note deleted!')
    return redirect(url_for('notes'))


@app.route('/pdf', methods=['GET'])
@login_required
def pdf():

    notes = Note.query.filter_by(user_id=g.user.id).order_by(Note.call_date.desc()).all()
    pdf = create_pdf(render_template('pdfTemplate.html', notes=notes))

    response = make_response(pdf)
    response.headers['Content-Disposition'] = "attachment; filename='file.pdf"
    response.mimetype = 'application/pdf'

    return response


@app.route('/sendPdf', methods=['GET'])
@login_required
def sendPdf():

    notes = Note.query.filter_by(user_id=g.user.id).order_by(Note.call_date.desc()).all()
    pdf = create_pdf(render_template('pdfTemplate.html', notes=notes))

    #send_email(g.user.email, pdf)

    flash('Email sent!')
    return redirect(url_for('notes'))


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():

    if request.method == 'GET':
        return render_template('forgotPassword.html')

    username = str(request.form['username'])

    token = ts.dumps(username, salt='username-confirm-key')

    reset_url = url_for(
        'reset_password',
        token=token,
        _external=True)

    return render_template(
        'activatePassword.html',
        reset_url=reset_url)


@app.route('/reset_password/<token>')
def reset_password(token):

    try:
        username = ts.loads(token, salt="username-confirm-key", max_age=86400)
    except:
        abort(404)

    return render_template('changePassword.html', username = username)


@app.route('/reset', methods=['POST'])
def reset():

    username = str(request.form['username'])
    password = str(request.form['password'])

    update_password(username, password)

    flash('Password changed!')
    return render_template('login.html')
