from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phonebook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class PhoneNumbers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(30))
    middleName = db.Column(db.String(30))
    lastName = db.Column(db.String(30), nullable=True)
    number = db.Column(db.String(30), unique=True)

    def __repr__(self):
        return f"<peoples {self.id}>"


@app.route("/", methods=("POST", "GET"))
def index():
    allphones = PhoneNumbers.query.all()
    if request.method == "POST":
        try:
            PhoneNumbers.query.filter(PhoneNumbers.id == request.form['delete_id_{{loop.index}}']).delete()
            db.session.flush()
            db.session.commit()
        except Exception:
            db.session.rollback()
            print("Error in deleting in DataBase")
    return render_template("index.html", title="Phonebook", list=allphones)


@app.route("/insertion", methods=("POST", "GET"))
def insertion():
    if request.method == "POST":
        try:
            phone = PhoneNumbers(firstName=request.form['firstname_name'],
                                 middleName=request.form['middlename_name'],
                                 lastName=request.form['lastname_name'],
                                 number=request.form['number_name'])

            db.session.add(phone)
            db.session.flush()
            db.session.commit()
        except Exception:
            db.session.rollback()
            print("Error in insertion in DataBase")
    return render_template("insertion.html", title="Insertion")


@app.route("/removal", methods=("POST", "GET"))
def removal():
    if request.method == "POST":
        try:
            PhoneNumbers.query.filter(PhoneNumbers.id == request.form['id']).delete()
            db.session.flush()
            db.session.commit()
        except Exception:
            db.session.rollback()
            print("Error in removal from DataBase")
    return render_template("removal.html", title="Removal")


if __name__ == "__main__":
    app.run(debug=True)
