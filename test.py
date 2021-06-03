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

    def __init__(self, name, age, gender, email):
        self.Name = name
        self.Age = age
        self.Gender = gender
        self.email = email


db.create_all()


# User Choice API


@app.route('/')
def user_choice():
    return render_template('userChoice.html')


@app.route('/choice', methods=['POST'])
def do_user_choice():
    try:
        choice = request.form.get('choice')
        if choice == 'add':
            return redirect(url_for('add_user_data'))
        elif choice == 'search':
            return redirect(url_for('search_user_data'))
        elif choice == 'view':
            return redirect(url_for('display_data'))
    except():
        print("Sorry !! Exception occurred")

# User Adding Data API


@app.route('/add')
def add_user_data():
    return render_template('userAddData.html')


@app.route('/add-data', methods=['POST'])
def add_data():
    try:
        user = Users(request.form.get('Name'), request.form.get('Age'),
                     request.form.get('Gender'), request.form.get('email'))
        db.session.add(user)
        db.session.commit()
        return "<html><body><h1>Data Added Successfully :)</h1><a href='/'>Go to Home Page</a></body></html>"
    except():
        print("Sorry Unhandled Exception")

# User search Data


@app.route('/search')
def search_user_data():
    return render_template('userSearchData.html')


@app.route('/no-result')
def display_no_results():
    return "<html><body><h1>No Results Found!!</h1><a href='/'>Go to Home Page</a></body></html>"


@app.route('/search-data', methods=['POST'])
def search_data():
    try:
        column = request.form.get('column')
        search_value = request.form.get('searchValue')
        gender_search_value = request.form.get('genderSearchValue')
        result_dict = {
            "desiredResult": [],
            "count": 0
        }
        column_names = ['Name', 'Age', 'Gender', 'email']

        if column == 'Name':
            query = Users.query.filter(Users.Name.contains(f'{search_value}')).all()
        elif column == 'Age':
            query = Users.query.filter(Users.Age.contains(f'{search_value}')).all()
        elif column == 'Gender':
            query = Users.query.filter(Users.Gender.contains(f'{gender_search_value}')).all()
        elif column == 'email':
            query = Users.query.filter(Users.email.contains(f'{search_value}')).all()
        else:
            query = []

        for record in query:
            record_dict = {}
            name, age, gender, email = record.Name, record.Age, record.Gender, record.email
            record_dict['Name'] = name
            record_dict['Age'] = age
            record_dict['Gender'] = gender
            record_dict['email'] = email
            result_dict['desiredResult'].append(record_dict)
            result_dict['count'] += 1

        if result_dict['count'] == 0:
            return redirect(url_for('display_no_results'))
        else:
            return render_template('displayResult.html', result=result_dict, colNames=column_names)
    except():
        print("Sorry Unhandled exception")


@app.route('/display', methods=['GET'])
def display_data():
    try:
        result_dict = {
            "desiredResult": [],
            "count": 0
        }
        column_names = ['Name', 'Age', 'Gender', 'email']

        query = Users.query.all()

        for record in query:
            record_dict = {}
            name, age, gender, email = record.Name, record.Age, record.Gender, record.email
            record_dict['Name'] = name
            record_dict['Age'] = age
            record_dict['Gender'] = gender
            record_dict['email'] = email
            result_dict['desiredResult'].append(record_dict)
            result_dict['count'] += 1

        return render_template('displayResult.html', result=result_dict, colNames=column_names)
    except():
        print("Sorry Unhandled Exception")


if __name__ == '__main__':
    app.run(debug=True)
