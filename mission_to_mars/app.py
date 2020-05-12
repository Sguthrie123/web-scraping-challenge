from flask import Flask, render_template, redirect
import pymongo
import scrape


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.MarsDB

app = Flask(__name__)

@app.route('/')
def home():
    
    mars = db.db.collection.find()
    return render_template("index.html", mars = mars )

@app.route('/scrape')
def scraper():

    mars_data = scrape.scrape()

    db.db.collection.update({} ,mars_data ,upsert=True )

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)