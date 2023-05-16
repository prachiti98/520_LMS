from flask.templating import render_template
from flask import Blueprint,current_app
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from views import view
from models import details


bookslist_blueprint = Blueprint('bookslist_blueprint', __name__)

# Creating the Books list
@bookslist_blueprint.route('/bookslist')
# @is_logged_in
def bookslist():
    mysql = current_app.config['mysql']
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