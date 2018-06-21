Web Scraping with Python, HTML, Flask, MongoDB, Splinter, BeautifulSoup

With this project I learned how to pull data from another website and display it on my own website.

A Flask server manages the relationship between the HTML webpage, my python file that pulls and saves the data into a Mongo database, and the Mongo database. The user clicks a 'scrape' button on the HTML page, which then tells Flask to run the scrape function in my python file, save the data in Mongo, and return the data to the HTML page. This presents live info from NASA on my own webpage.

The scrape function in the python file uses the Splinter and BeautifulSoup libraries. Splinter helps run a mock browser to visit websites and see what the code is doing, while BeautifulSoup is used to extract information from the page's HTML.
