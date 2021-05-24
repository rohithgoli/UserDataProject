from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv

app = Flask(__name__)

# User Choice API


@app.route('/')
def user_choice():
    return render_template('userChoice.html')


@app.route('/choice', methods = ['POST','GET'])
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


@app.route('/add-data', methods = ['POST','GET'])
def add_data():
    if request.method == 'POST':
        Name = request.form['Name']
        Age = request.form['Age']
        Gender = request.form['Gender']
        email = request.form['email']
        with open('users.csv', 'a+', newline='') as csv_file:
            fieldnames = ['Name', 'Age', 'Gender', 'email']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'Name': Name, 'Age': Age, 'Gender': Gender, 'email': email})
        return "Data submitted successfully!! :)"

# User Searching Data API


@app.route('/search')
def search_user_data():
    return render_template('userSearchData.html')


@app.route('/no-result')
def display_no_results():
    return '<html><body><h1>No Results Found!!</h1></body></html>'


@app.route('/search-data', methods=['POST', 'GET'])
def search_data():
    if request.method == 'POST':
        column = request.form['column']
        searchValue = request.form['searchValue']
        result_dict = {
            "desiredResult": [],
            "count": 0
        }

        with open('users.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            columnNames = csv_reader.fieldnames
            for row in csv_reader:
                if searchValue in row[column]:
                    result_dict['desiredResult'].append(row)
                    result_dict['count'] += 1
            if result_dict['count'] == 0:
                return redirect(url_for('display_no_results'))
            else:
                #return jsonify(result_dict)
                return render_template('displayResult.html',result = result_dict, colNames = columnNames)

# Displaying User Data API


@app.route('/display', methods = ['GET'])
def display_data():
    if request.method == 'GET':
        result_dict = {
            'count':0,
            'desiredResult':[]
            }
        with open('users.csv','r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            columnNames = csv_reader.fieldnames
            for row in csv_reader:
                result_dict['desiredResult'].append(row)
                result_dict['count'] += 1
        #return (jsonify(result_dict))
        return render_template('displayResult.html',result = result_dict, colNames = columnNames)


if __name__ == '__main__':
    app.run(debug = True)
