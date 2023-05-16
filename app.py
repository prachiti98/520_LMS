from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from views import view
from models import details
from controllers.index import index_blueprint

app = Flask(__name__)
#/home/mugdha/Projects/Library_Management_System/config.py
app.config.from_pyfile('D:\Library-Management-System\config.py')

# Initializing MySQL
mysql = MySQL(app)


app.register_blueprint(index_blueprint)

# @app.route('/')
# def index():
#     return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')



#User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
        currentStudentDetails = details.StudentDetail()
        form = view.RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
            currentStudentDetails.studentName = form.studentName.data
            currentStudentDetails.email = form.email.data
            currentStudentDetails.mobile = form.mobile.data
            currentStudentDetails.studentUsername = form.studentUsername.data
            currentStudentDetails.password = sha256_crypt.hash(str(form.password.data))

            # Creating the cursor
            cur = mysql.connection.cursor()

            # print(password)

            # Executing Query
            cur.execute("INSERT INTO students(studentName, email, mobile, studentUsername, password) VALUES(%s, %s, %s, %s, %s)", \
                        (currentStudentDetails.studentName, currentStudentDetails.email, currentStudentDetails.mobile, currentStudentDetails.studentUsername, currentStudentDetails.password))

            
            # Commit to database
            mysql.connection.commit()

            # Close connection
            cur.close()

            flash("You are now registered.", 'success')

            return redirect(url_for('login'))

        return render_template('register.html', form= form )

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        currentStudentDetail = details.StudentDetail()
        #Get form fields
        currentStudentDetail.studentUsername = request.form['studentUsername']
        currentStudentDetail.password = request.form['password']

        # Create Cursor
        cur = mysql.connection.cursor()

        # Get user by Username
        result = cur.execute("SELECT * FROM students WHERE studentUsername = %s", [currentStudentDetail.studentUsername])

        if result > 0:

            # Get the stored hash
            data = cur.fetchone()
            originalPassword = data['password']


            # Comparing the Passwords
            if sha256_crypt.verify(currentStudentDetail.password, originalPassword):

                # Password matched
                session['logged_in'] = True
                session['studentUsername'] = currentStudentDetail.studentUsername
                # session['aadharNo'] = data['aadharNo']

                flash('You have successfully logged in', 'success')
                return redirect(url_for('bookslist'))

            else:
                error = 'Invalid login.'
                return render_template('login.html', error = error)

            #Close connection
            cur.close()

        else:
            error = 'Username not found.'
            return render_template('login.html', error = error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, please Login.', 'danger')
            return redirect(url_for('login'))
    return wrap

# Creating the Books list
@app.route('/bookslist')
# @is_logged_in
def bookslist():

    # Create Cursor
    cur = mysql.connection.cursor()

    # Execute
    result = cur.execute("SELECT bookName, sum(available) AS count FROM books GROUP BY bookName")

    books = cur.fetchall()

    if result > 0:
        return render_template('bookslist.html', books = books)
    else:
        msg = 'No books found'
        return render_template('bookslist.html', msg= msg)

    # Close connection
    cur.close()

# Personal Details
@app.route('/student_detail')
@is_logged_in
def student_detail():

    # Create Cursor
    cur = mysql.connection.cursor()

    # Execute
    result = cur.execute("SELECT * FROM transactions WHERE studentUsername = %s", (session['studentUsername'], )) 

    transactions = cur.fetchall()
    fine_result = cur.execute("select fine from transactions where studentUsername like %s",(session['studentUsername'], ))
    fine=cur.fetchone()
    
    if result > 0 and fine_result > 0:
        return render_template('student_detail.html', transactions = transactions,fine=fine['fine'])
    elif result > 0:
        return render_template('student_detail.html', transactions = transactions,fine=0)
    else:
        msg = 'No recorded transactions'
        return render_template('student_detail.html', msg= msg)

    # Close connection
    cur.close()

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You have logged out.', 'success')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(host = '0.0.0.0', port = 5001, debug=True)
