from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import requests
import pandas as pd
from flask_cors import CORS
import sqlite3
import os

# this function can be used to create the product sqlite database if necessary
def createdb():
    with sqlite3.connect("productdb.db") as con:
        with open("initscript.sql") as f:
            con.executescript(f.read())

# Here, we check if the product database already exists 
# If it does, we will continue our app per usual, adding new data to the exsisting db
# If it does not, we will create it for the first time
# We don't want to create a new database every single time becuase the whole purpose of this program is to be able to add to and retrieve data from an existing db 
if not os.path.exists('productdb.db'):
    createdb()

# creating the Flask 
app = Flask(__name__, template_folder='templates')
CORS(app)

# creating the "Home" page for route "/"
@app.route('/', methods=['GET'])
def selection():
    return render_template("home.html",title="Home") # will return the "home.html" template, i.e. the selection menu

# ------------------------------------------------------------------------------------------------------------------------
# DATA ENTRY 

# creating a route for if any errors occur in adding information into the sqlite db
# renders an html of a custom error page 
@app.route('/error', methods=['POST'])
def error():
    return render_template("unique.html", title="Error")

# renders the html template of the data entry form
@app.route('/dataentry', methods=['GET'])
def entryform():
    return render_template("dataentry.html",title="Product Data Entry")

# takes the data from the 'dataentry' form and processes it into a sqlite database
@app.route('/entryprocessing', methods=['POST'])
def postentry():

    # tries to proceed how intended
    try: 
        # grabbing the variables from the form
        category = request.form.get("category")
        description = request.form.get("description")
        price = request.form.get("price")
        code = request.form.get("code")

        # creating a list of a tuple of all of the form values to prevent automatic SQL escaping 
        # this also makes the insert statement shorter/simpler
        to_insert = [(category, description, price, code)]

        # connecting to our database to execute the values grabbed from the form into the table
        with sqlite3.connect("productdb.db") as con:
            con.executemany("INSERT INTO product VALUES (?,?,?,?)", to_insert)
    
    # if an exception is thrown (i.e. an integrity issue), the error() function (above) is called 
    except:
        return error()

    # once this process is done, the user is returned to the home page 
    return render_template("home.html",title="Home")        

# ------------------------------------------------------------------------------------------------------------------------
# DATA RETRIEVAL

# renders the html template of the data retrieval form
@app.route('/dataretrieval', methods=['GET'])
def dataretrieval():
    return render_template("dataretrieval.html",title="Product Data Entry")

# takes the user desired category from the 'dataretireval' form and uses it to filter the sqlite3 db
@app.route('/list', methods=['POST'])
def list():

    # grabbing the user-entered variable from the form
    # stripping the variable to prevent any issues with spaces from occuring 
    catdes = request.form.get("category").strip()

    # connecting to the sqlite3 db
    with sqlite3.connect("productdb.db") as con:

        # if structure to determine what to display
        # if the user leaves the category selection input box blank, the entire product table will be displayed
        
        if catdes != "":
            # display only rows of the table that have the desired category
            df = pd.read_sql("SELECT * FROM product WHERE category=?", con, params=(catdes,)) # coverting the db to a pandas db & filtering it by the query of the category
        else:
            # display all rows of the table 
            df = pd.read_sql("SELECT * FROM product", con)

    return render_template("postdata.html", df=df, title="Retrieval from Database")


#app.run(debug=True, port=8080) 

