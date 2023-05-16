from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from views import view
from models import details


register_blueprint = Blueprint('register_blueprint', __name__)



@register_blueprint.route("/register", methods=['GET', 'POST'])
#User Registration
def register():
        mysql = current_app.config['mysql']
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