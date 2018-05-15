
#Import BeautifulSoup and Splinter for Webscraping and HTML editing capabilities
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


# In[41]:


# Path to chromedriver
#get_ipython().system('which chromedriver')


def initBrowser():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': '/Users/thomashague/Desktop/data/webScrapingAndDocumentDatabases/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

# put all operations from jupyter file into one scrape function, which returns the scraped data in a dictionary
def scrape():
    browser = initBrowser()
    mars = {}

    # ==========Get the latest news article==========
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Use beautiful soup to find the first news title parent element
    listTextLabelElem = news_soup.find('div', class_='list_text')

    # Use the parent element to find the first a tag and save it as `news_title`. Add to mars dict
    mars['news_title'] = listTextLabelElem.find('a').get_text()

    # Use the parent element to find the paragraph text
    listTextLabelElem = news_soup.find('div', class_='article_teaser_body')
    mars['news_p'] = listTextLabelElem.get_text()

    # ==========Get the JPL Mars featured image==========
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Now that splinter is on the web page we're looking for, parse the html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # Find the relative link to the main image
    img_url_rel = img_soup.find('figure', class_='lede').find('img')['src']

    # add to the base url to create an absolute path
    mars['featuredImage'] = f'https://www.jpl.nasa.gov{img_url_rel}'

    # ==========Get the weather on Mars from Twitter==========

    # As usual, start with the URL and visit it with browser
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # use soup to parse the html
    html = browser.html
    weather_soup = BeautifulSoup(html,'html.parser')

    # First, find a tweet with the data-name `Mars Weather`
    mars_weather_tweet = weather_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})

    # Next, search within the tweet for the p tag containing the tweet text
    mars['mars_weather'] = mars_weather_tweet.find('p', 'tweet-text').get_text()

    # ========== Mars Hemispheres ==========

    # As usual, start with the URL and visit it with browser
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Array where final urls will be stored
    hemisphere_image_urls = []

    # Where the correct links show up in list of links
    sequence = [1,3,5,7]

    # Loop to get all 4 hemisphere image urls
    for i in sequence:
        
        # First, get a list of all of the hemispheres
        links = browser.find_link_by_partial_href("/search/map/Mars/Viking/")

        hemisphere = {}
        
        # Navigate to image page
        links[i].click()

        # Find the Sample image anchor tag and extract the href
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']

        # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text

        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)

        # Finally, navigate backwards
        browser.back()
        
        # Wait for the page to load
        time.sleep(5)   

    # Add the hemisphere links to the dict as one object
    mars['hemispheres'] = hemisphere_image_urls

    #create a dataframe from the html table
    df = pd.read_html('http://space-facts.com/mars/')[0]
    df.columns=['description', 'value']
    df.set_index('description', inplace=True)

    # Convert dataframe to html, replace new line symbols with spaces, add html to dict
    table = df.to_html()
    table = table.replace('\n', '')
    mars['facts'] = table

    browser.quit()

    return mars

