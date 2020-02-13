from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import copy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres:danielking17post29@localhost:1234/project1'
db = SQLAlchemy(app)


class booksdb(db.Model):
    __tablename__ = "booksdb"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)



class readerdb(db.Model):
    __tablename__ = "readerdb"
    user_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def add_book(self, isbn, title, author, year):
        b = booksdb(isbn=isbn, title=title, author=author, year=year)
        db.session.add(b)
        db.session.commit()


db.create_all()

db_string = 'postgres+psycopg2://postgres:danielking17post29@localhost:1234/project1'
engine = create_engine(db_string)
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        if (year == "year"):
            continue
        db.add(booksdb(isbn=isbn, title=title, author=author, year=year))
        db.commit()
    db.commit()
