from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
from pymongo import MongoClient
import scrape_mars
from pymongo import MongoClient

connection = MongoClient('localhost', 27017) #Connect to mongodb
db = connection['Mars_app'] 

#db.collection.delete_many({})
#db.collection.insert_one(data)
#if "Mars" in db.list_collection_names:
collection = db['Mars_data']
if collection.count() == 0:
    print("First time inserting data into the empty Mongodb Mars database!")
    data = scrape_mars.scrape()  
    collection.insert_one(data)
else:
    print("Mars data reading from Mongodb Mars database!")

# create instance of Flask app
app = Flask(__name__)

#mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_app")

# create route that renders index.html template
@app.route("/")
def index():
    mars_collection_values=collection.find_one()
    return render_template("index.html",Mars = mars_collection_values)

@app.route('/scrape')
def scrape():
    data = scrape_mars.scrape()  
    #db.collection.delete_many({})
    #db.collection.insert_one(data)
    # return redirect("http://localhost:5000/", code=302)
    # Update the Mongo database using update and upsert=True
    collection.update({}, data, upsert=True)
    return redirect('/')


@app.route('/Mars_facts')
def facts():
    mars_collection_values=collection.find_one()
    return render_template("Mars_facts.html",Mars = mars_collection_values)


@app.route('/Mars_news')
def news():
    mars_collection_values=collection.find_one()
    return render_template("Mars_news.html",Mars = mars_collection_values)

@app.route('/Mars_weather')
def weather():
    mars_collection_values=collection.find_one()
    return render_template("Mars_weather.html",Mars = mars_collection_values)

if __name__ == "__main__":
    app.run(debug=True)