# Import Dependencies
from flask import Flask, render_template, redirect
import pymongo
import scrape

# Establish Connection 
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.MarsDB

# Start the flask app
app = Flask(__name__)

# Define route 
@app.route('/')
def home():
    # find the db collection and render it 
    mars = db.db.collection.find()
    return render_template("index.html", mars = mars )

@app.route('/scrape')
def scraper():
    # Run the scrape function we made to pull all the data from the sources 
    mars_data = scrape.scrape()
    # Update the collection with new data 
    db.db.collection.update({} ,mars_data ,upsert=True )

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)