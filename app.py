from flask import Flask, render_template, redirect
# Import scrape_mars
import scrape_mars

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
#conn = 'mongodb://localhost:27017'
mongo = PyMongo(app, uri='mongodb://localhost:27017/mission_to_mars')

# Pass connection to the pymongo instance.

# Set route
@app.route("/")
def index():
    mars_data = mongo.db.mars_collection.find_one() 
    return render_template("index.html", mars_data=mars_data)

# Scrape 
@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_collection
    mars_data.mars_collection.remove({})
    new_mars_data = scrape_mars.scrape()
    mars_data.update({}, new_mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
  