# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time


def scrape():
    # This is to initialize Splinter for Mac users
    #https://splinter.readthedocs.io/en/latest/drivers/chrome.html
    #!which chromedriver
    

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    # Run the function below:
    news_headline, news_teaser = mars_news(browser)
    
    # Run the functions below and store into a dictionary
    results = {
        "title": news_headline,
        "paragraph": news_teaser,
        "image_URL": mars_space_image(browser),
        "weather": mars_weather_tweet(browser),
        "facts": mars_facts(),
        "hemispheres": mars_hemispheres(browser),
    }

    # Quit the browser and return the scraped results
    #browser.quit()
    return results

def mars_news(browser):
    # Visit the following URL
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)


    # Create BeautifulSoup object; parse with 'html.parser'
    time.sleep(1)
    nasa_html = browser.html
    nasa_soup = BeautifulSoup(nasa_html, 'html.parser')

    #Scrape the first article and teaser paragraph from the page
    news_list = nasa_soup.find('ul', class_='item_list')
    first_item = news_list.find('li', class_='slide')
    news_headline = first_item.find('div', class_='content_title').text
    news_teaser = first_item.find('div', class_='article_teaser_body').text
    
    return news_headline, news_teaser

def mars_space_image(browser):
    # Visist the url for the page to scrape
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Click the image to display the full picture
    time.sleep(1)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    expand = browser.find_by_css('a.fancybox-expand')
    expand.click()
    time.sleep(1)

    # Scrape the featured image
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')

    img_relative = jpl_soup.find('img', class_='fancybox-image')['src']
    featured_image_url = f'https://www.jpl.nasa.gov{img_relative}'

    return featured_image_url

def mars_weather_tweet(browser):
    # Url for the twitter page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    time.sleep(1)
    html = browser.html
    tweet_soup = BeautifulSoup(html, 'html.parser')

    # Scrape the latest tweet
    mars_weather = tweet_soup.find('p', class_='TweetTextSize').text

    return mars_weather

def mars_facts():
    # URL for the mars facts table
    url = 'https://space-facts.com/mars/'
    # use pandas to read the table
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = ["Description", "Value"]
    df.set_index("Description", inplace=True, drop=True)

    # Convert the pandas table to an HTML table string
    mars_facts_html = df.to_html()

    # Clean up HTML
    mars_facts_html = mars_facts_html.replace("\n","")

    return mars_facts_html

def mars_hemispheres(browser):
    # URL of page to be scraped
    base_hemisphere_url = "https://astrogeology.usgs.gov"
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    # Create BeautifulSoup object; parse with 'html.parser'
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Create a list with the links for the hemispheres
    hemisphere_image_urls = []

    links = soup.find_all("div", class_="item")

    for link in links:
        img_dict = {}
        title = link.find("h3").text
        next_link = link.find("div", class_="description").a["href"]
        full_next_link = base_hemisphere_url + next_link
    
        browser.visit(full_next_link)
    
        pic_html = browser.html
        pic_soup = BeautifulSoup(pic_html, 'html.parser')
    
        url = pic_soup.find("img", class_="wide-image")["src"]

        img_dict["title"] = title
        img_dict["img_url"] = base_hemisphere_url + url

    
        hemisphere_image_urls.append(img_dict)

    return hemisphere_image_urls




