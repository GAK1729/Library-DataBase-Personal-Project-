import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from createReaderDB import *
from sqlalchemy import and_, or_



app = Flask(__name__)

db_string = 'postgres+psycopg2://postgres:dking17post29@localhost:1234/project1'
engine = create_engine(db_string)

db = scoped_session(sessionmaker(bind=engine))

def loginCheck(userName, password):
    un = db.query(readerdb).get(userName)
    if ( None == un ):
        print("Invalid UserName ")
        return (False, 1)
    if( password != un.password):
        print("Invalid Password ")
        return (False, 2)
    return (True, 3)

def searchOutput(book_id, title, author):
    x = "Choose an Option"
    if(book_id == "Choose an Option" and author != x and title != x):
        print(1)
        q = db.query(booksdb).filter(and_(booksdb.title == title, booksdb.author == author)).all()

    elif(title == "Choose an Option" and book_id != x and author != x):
        print(2)
        q = db.query(booksdb).filter(and_(booksdb.isbn == book_id, booksdb.author == author)).all()

    elif(author == "Choose an Option" and book_id != x and title != x):
        print(3)
        q = db.query(booksdb).filter(and_(booksdb.isbn == book_id, booksdb.title == title)).all()

    elif(book_id == "Choose an Option" and title == "Choose an Option" and author != x):
        print(4)
        q = db.query(booksdb).filter(booksdb.author == author).all()

    elif(author == "Choose an Option" and book_id == "Choose an Option" and title != x):
        print(5)
        q = db.query(booksdb).filter(booksdb.title == title).all()

    elif(title == "Choose an Option" and author == "Choose an Option" and book_id != x):
        print(6)
        q = db.query(booksdb).filter(booksdb.isbn == book_id).all()
    return q


@app.route("/")
@app.route("/home")
def theReaderHome():
    return render_template("theReaderHome.html", message= "work")


@app.route("/SignUp")
def signUp():
    """Sign Up."""
    return render_template("signUp.html")

@app.route("/User", methods=["POST"])
def newUser():
    """Sign Up."""
    user_id = request.form['user ID']
    name = request.form['Name']
    password = request.form['password']
    db.add(readerdb( user_id=user_id, name=name, password=password))
    db.commit()
    return render_template("theReaderHome.html")



@app.route("/loginAttempt/", methods=["POST"])
def loginAttempt():
    """Sign Up."""
    user_id = request.form['username']
    # name = request.form['Name']
    password = request.form['password']
    # return render_template("loggedIn.html", name = user_id)
    sf =  loginCheck(userName = user_id, password = password)
    if(sf[0]):
        temp = db.query(readerdb).get(user_id)
        name = temp.name
        allBooks =db.query(booksdb).all()
        return render_template("loggedIn.html",allBooks = allBooks, user_id = user_id, name = name)
    elif(sf[1] == 1):
        return render_template("theReaderHome.html", wrong = "Invalid UserName")
    elif(sf[1] == 2):
        return render_template("theReaderHome.html", wrong = "Invalid Password")


@app.route("/search", methods=["POST"])
def searchBook():
    """Searching ."""
    book_id = request.form.get('bookID')
    title = request.form.get('title')
    author = request.form.get('Author')
    allBooks =db.query(booksdb).all()
    searchResultList = searchOutput(book_id, title, author)
    return render_template("loggedIn.html", searchResultList = searchResultList, allBooks = allBooks)

if __name__ == '__main__':
	app.run(debug=True, port=4000)
