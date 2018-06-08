# Import flask to create a server that can display data
from flask import Flask, render_template, jsonify, redirect
# Import flask_pymongo to be able to pull fom the Mongo database
from flask_pymongo import PyMongo
# Import python file that pulls all the data from web and puts it into Mongo database
import webScrape

# Create the Flask app
app = Flask(__name__)

# Create the Mongo object
mongo = PyMongo(app)

# Create the default app route
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    mars_data = webScrape.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)


    # Why isnt this working??? Is it this file or my webScrape file?