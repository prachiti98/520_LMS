from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from views import view
from models import details
from flask import Blueprint,current_app
from controllers.bookslist import bookslist_blueprint

login_blueprint = Blueprint('login_blueprint', __name__)

# User Login
@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mysql = current_app.config['mysql']
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
                return redirect(url_for('bookslist_blueprint.bookslist'))

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

studentdetail_blueprint = Blueprint('studentdetail_blueprint', __name__)

# Personal Details
@studentdetail_blueprint.route('/student_detail')
@is_logged_in
def student_detail():
    mysql = current_app.config['mysql']
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

logout_blueprint = Blueprint('logout_blueprint', __name__)

# Logout
@logout_blueprint.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You have logged out.', 'success')
    return redirect(url_for('login_blueprint.login'))
