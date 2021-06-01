from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
db = SQLAlchemy(app)


class Users(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Age = db.Column(db.Integer)
    Gender = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def __init__(self, Name, Age, Gender, email):
        self.Name = Name
        self.Age = Age
        self.Gender = Gender
        self.email = email


db.create_all()


# User Choice API


@app.route('/')
def user_choice():
    return render_template('userChoice.html')


@app.route('/choice', methods=['POST'])
def do_user_choice():
    if request.method == 'POST':
        choice = request.form['choice']
        if choice == 'add':
            return redirect(url_for('add_user_data'))
        elif choice == 'search':
            return redirect(url_for('search_user_data'))
        elif choice == 'view':
            return redirect(url_for('display_data'))


# User Adding Data API


@app.route('/add')
def add_user_data():
    return render_template('userAddData.html')


@app.route('/add-data', methods=['POST'])
def add_data():
    if request.method == 'POST':
        user = Users(request.form['Name'], request.form['Age'], request.form['Gender'], request.form['email'])
        db.session.add(user)
        db.session.commit()
        return "Data Added Successfully :) "


# User search Data

@app.route('/search')
def search_user_data():
    return render_template('userSearchData.html')


@app.route('/no-result')
def display_no_results():
    return '<html><body><h1>No Results Found!!</h1></body></html>'


@app.route('/search-data', methods=['POST'])
def search_data():
    if request.method == 'POST':
        column = request.form['column']
        searchValue = request.form['searchValue']
        result_dict = {
            "desiredResult": [],
            "count": 0
        }
        columnNames = ['Name', 'Age', 'Gender', 'email']

        if column == 'Name':
            query = Users.query.filter(Users.Name.contains(f'{searchValue}')).all()
        elif column == 'Age':
            query = Users.query.filter(Users.Age.contains(f'{searchValue}')).all()
        elif column == 'Gender':
            query = Users.query.filter(Users.Gender.contains(f'{searchValue}')).all()
        elif column == 'email':
            query = Users.query.filter(Users.email.contains(f'{searchValue}')).all()
        else:
            query = []

        for record in query:
            record_dict = {}
            Name, Age, Gender, email = record.Name, record.Age, record.Gender, record.email
            record_dict['Name'] = Name
            record_dict['Age'] = Age
            record_dict['Gender'] = Gender
            record_dict['email'] = email
            result_dict['desiredResult'].append(record_dict)
            result_dict['count'] += 1

        if result_dict['count'] == 0:
            return redirect(url_for('display_no_results'))
        else:
            # return jsonify(result_dict)
            return render_template('displayResult.html', result=result_dict, colNames=columnNames)


@app.route('/display', methods=['GET'])
def display_data():
    if request.method == 'GET':
        result_dict = {
            "desiredResult": [],
            "count": 0
        }
        columnNames = ['Name', 'Age', 'Gender', 'email']

        query = Users.query.all()

        for record in query:
            record_dict = {}
            Name, Age, Gender, email = record.Name, record.Age, record.Gender, record.email
            record_dict['Name'] = Name
            record_dict['Age'] = Age
            record_dict['Gender'] = Gender
            record_dict['email'] = email
            result_dict['desiredResult'].append(record_dict)
            result_dict['count'] += 1

        return render_template('displayResult.html', result=result_dict, colNames=columnNames)


if __name__ == '__main__':
    app.run(debug=True)