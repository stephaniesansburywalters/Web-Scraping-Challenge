#Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

#Root
def init_browser():
    executable_path = {"executable_path":r"C:\Users\steph\Downloads\chromedriver_win32\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

#Scraping Function
def scrape_info():
    browser = init_browser()

    #Declares Mars News URL
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")
    

    #Scrape for Title and Paragraph
    news_title = soup.find("div", class_="content_title").get_text()
    news_p = soup.find("div", class_ ="article_teaser_body").get_text()

    #Declares URL for JPL NASA Images
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    time.sleep(5)
    
    #Clicks Buttons
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    html = browser.html
    soup = bs(html, "html.parser")

    #Scrapes for Images
    image = soup.find("img", class_="main_image")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    
    #Declares Mars Twitter
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    time.sleep(5)
    html = browser.html
    w_soup = bs(html, "html.parser")

    #Scrapes for Mars Tweets
    weather_tweet =  w_soup.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})
    weather = weather_tweet.find('p', 'tweet-text').get_text()

    #Declare Mars Facts URL
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")

    #Scrapes for Mars Facts
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_facts = mars_data.to_html(header = False, index = False)

    #Declares URL for Hemispheres
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    time.sleep(5)
    html = browser.html
    soup = bs(html, "html.parser")

    #Creates Empty List
    hemisphere_image_urls  = []

    #Points to Hemispheres
    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    #Loops Through Hemispheres
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").get_text()
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a", class_="product-item")["href"]
        image_link = "https://astrogeology.usgs.gov" + end_link
           
        browser.visit(image_link)
        html = browser.html
        w_soup = bs(html, "html.parser")
        image_url = soup.find("img", class_="wide-image")["src"]
        image_url = "https://astrogeology.usgs.gov" + image_url
        
        hemisphere_image_urls.append({"title": title, "image_url": image_url})

    #Creates Collection for Database   
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "weather": weather,
        "mars_facts": mars_facts,
        "featured_image_url": featured_image_url,
        "hemisphere_image_urls":hemisphere_image_urls
    }

    #Closes Browser After Scraping
    browser.quit()

    #Returns Data
    return mars_data