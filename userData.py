from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# User Choice API


@app.route('/')
def user_choice():
    return render_template('userChoice.html')


@app.route('/choice', methods=['POST'])
def do_user_choice():
    try:
        choice = request.form['choice']
        if choice == 'add':
            return redirect(url_for('add_user_data'))
        elif choice == 'search':
            return redirect(url_for('search_user_data'))
        elif choice == 'view':
            return redirect(url_for('display_data'))
        else:
            raise ValueError
    except ValueError:
        print("Invalid choice :(")


# User Adding Data API


@app.route('/add')
def add_user_data():
    return render_template('userAddData.html')


@app.route('/add-data', methods=['POST'])
def add_data():
    try:
        name = request.form.get('Name')
        age = request.form.get('Age')
        gender = request.form.get('Gender')
        email = request.form.get('email')
        with sqlite3.connect('users.db') as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO users(Name,Age,Gender,email)\
                            VALUES (?,?,?,?)", (name, age, gender, email))
            con.commit()
        msg = "Data Added successfully!! :)"

    except():
        con.rollback()
        msg = ":( Error in Adding Data !!"

    finally:
        con.close()
        return f"{msg}"

# User Searching Data API


@app.route('/search')
def search_user_data():
    return render_template('userSearchData.html')


@app.route('/no-result')
def display_no_results():
    return '<html><body><h1>No Results Found!!</h1></body></html>'


@app.route('/search-data', methods=['POST'])
def search_data():
    if request.method == 'POST':
        try:
            column = request.form['column']
            search_value = request.form['searchValue']
            result_dict = {
                "desiredResult": [],
                "count": 0
            }

            with sqlite3.connect('users.db') as con:
                con.row_factory = sqlite3.Row
                cursor = con.cursor()
                cursor.execute(f"SELECT * FROM users WHERE {column} LIKE '%{search_value}%' ")
                rows = cursor.fetchall()
                for each_row in rows:
                    result_dict['count'] += 1
                    user_dict = {}
                    column_names = each_row.keys()
                    for key in column_names:
                        user_dict[key] = each_row[key]
                    result_dict['desiredResult'].append(user_dict)

            if result_dict['count'] == 0:
                return redirect(url_for('display_no_results'))
            else:
                return render_template('displayResult.html', result=result_dict, colNames=column_names)
        except:
            con.rollback()
        finally:
            con.close()


# Displaying User Data API


@app.route('/display', methods=['GET'])
def display_data():
    try:
        result_dict = {
            'count': 0,
            'desiredResult': []
            }
        with sqlite3.connect('users.db') as con:
            con.row_factory = sqlite3.Row
            cursor = con.cursor()
            cursor.execute("SELECT * FROM users;")
            rows = cursor.fetchall()

            for row in rows:
                result_dict['count'] += 1
                user_dict = {}
                column_names = row.keys()
                for key in column_names:
                    user_dict[key] = row[key]
                result_dict['desiredResult'].append(user_dict)
        return render_template('displayResult.html', result=result_dict, colNames=column_names)
    except:
        con.rollback()
    finally:
        con.close()


if __name__ == '__main__':
    app.run(debug=True)
