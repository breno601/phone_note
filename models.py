from sqlalchemy_utils.types.password import PasswordType
import datetime

from app import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],

        deprecated=['md5_crypt']
    ))
    email_confirmed = db.Column(db.Boolean, default=False)
    notes = db.relationship('Note', backref='user', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password


class Note(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone_number = db.Column(db.String(16))
    call_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    notes = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, phone_number, notes):
        self.name = name
        self.phone_number = phone_number
        self.notes = notes


def create_user(name, username, email, password):

    user = User(name, username, email, password)
    db.session.add(user)
    db.session.commit()

    return user


def confirm_user(email):

    user = User.query.filter_by(email=email).first_or_404()

    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return user


def update_password(username, password):

    user = User.query.filter_by(username=username).first_or_404()

    user.password = password
    db.session.add(user)
    db.session.commit()

    return user


def create_note(name, phone_number, note, user):

    note = Note(name, phone_number, note)
    note.user = user
    db.session.add(note)
    db.session.commit()

    return note


def delete_note(id):
    Note.query.filter_by(id=id).delete()
    db.session.commit()


def update_note(id, name, phone, notes):
    note = Note.query.filter_by(id=id).first()
    note.name = name
    note.phone_number = phone
    note.notes = notes
    db.session.commit()


if __name__ == "__main__":

    # Run this file directly to create the database tables.
    print "Creating database tables..."
    db.create_all()
    print "Done!"

    user = User("breno", "admin", "breno601@gmail.com", "tester123")
    user.email_confirmed = True
    user2 = User("breno2", "admin2", "breno602@gmail.com", "tester123")
    user2.email_confirmed = True
    db.session.add(user)
    db.session.add(user2)
    db.session.commit()

    note1 = Note("Breno", "638493594", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
    note1.user = user
    note2 = Note("John", "638493593", "Praesent mollis lacus in velit iaculis, sed ornare nisl laoreet. Curabitur accumsan ullamcorper ex volutpat malesuada. Nunc a viverra diam.")
    note2.user = user
    note3 = Note("Bohn", "638493592", "Pellentesque aliquam finibus tempor. Quisque commodo orci ut orci tempus dictum. Vivamus interdum ante vel dictum ullamcorper.")
    note3.user = user
    note4 = Note("Axl", "638493591", "Proin blandit, quam in suscipit pretium, elit sem ultrices lectus, vitae eleifend leo mauris et sapien. Vestibulum nec faucibus turpis, sit amet accumsan sem.")
    note4.user = user
    note5 = Note("Slash", "638493590", "Phasellus dignissim augue in vulputate facilisis. Nulla elit risus, viverra vel gravida ut, vestibulum id orci.")
    note5.user = user
    note6 = Note("Izzy", "638493589", "Donec vestibulum erat metus, eu mollis orci malesuada in. Donec eu porta orci.")
    note6.user = user
    note7 = Note("Fred", "638493588", "Aliquam laoreet ipsum justo, sed sagittis orci venenatis non.")
    note7.user = user
    note8 = Note("Test", "638493587", "Aliquam purus purus, pretium quis enim id, dapibus placerat neque.")
    note8.user = user
    note9 = Note("Juan", "638493586", "Etiam id egestas sapien, a malesuada dui. Integer ut dapibus leo, in rhoncus ante. In vel hendrerit massa.")
    note9.user = user
    note10 = Note("Pablo", "638493585", "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.")
    note10.user = user
    note11 = Note("Escobar", "638493584", "Morbi vulputate odio eget dapibus tempor. Aliquam consectetur pharetra quam ac fringilla.")
    note11.user = user
    note12 = Note("Pieter", "638493583", "Praesent iaculis porta interdum. Sed finibus sagittis tellus, scelerisque aliquam erat feugiat sit amet. ")
    note12.user = user
    note13 = Note("Robert", "638493582", "Praesent porttitor nunc vel justo fermentum, non fermentum ex laoreet. In hac habitasse platea dictumst.")
    note13.user = user
    note14 = Note("Nicholas", "638493581", "Proin et ornare nisi. Nam sagittis ultrices nisi, nec consequat turpis eleifend et.")
    note14.user = user
    note15 = Note("Cage", "638493580", "Proin a nibh in ante suscipit ultricies a nec odio.")
    note15.user = user
    note16 = Note("Tom", "638493579", "Proin rutrum egestas elit, nec facilisis ligula viverra sed. ")
    note16.user = user
    note17 = Note("Harry", "638493578", "Donec ipsum mi, ultrices ut urna ac, dapibus convallis ligula. Donec pharetra arcu ut cursus tempus.")
    note17.user = user
    note18 = Note("Joseph", "638493577", "Curabitur metus nisl, volutpat et consequat ac, volutpat at urna.")
    note18.user = user
    note19 = Note("Heisenberg", "638493576", "Duis interdum, leo non tincidunt ultrices, nulla lectus blandit sem.")
    note19.user = user
    db.session.add_all([note1, note2, note3, note4, note5, note6, note7, note8, note9, note10, note11, note12, note13, note14, note15, note16, note17, note18, note19])
    db.session.commit();
