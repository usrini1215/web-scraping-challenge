from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.select_one('ul.item_list li.slide div.content_title')
    news_p = soup.select_one('div.article_teaser_body')


    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser2 = init_browser()
    browser2.visit(url2)
    #delay next action by 5 sec..
    time.sleep(2)
    browser2.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
   
    html_jpl = browser2.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup_jpl = bs(html_jpl, 'html.parser')
    featured_image_url = (soup_jpl.select_one('img.fancybox-image')).get('src')
    print(f'image = {featured_image_url}')

    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url
    print(f'imagenow = {featured_image_url}')
    time.sleep(2)



    import re
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser3 = init_browser()
    browser3.visit(twitter_url)
    time.sleep(7)
    html_twit = browser3.html
    soup_twit = bs(html_twit, 'html.parser')
    mars_weather_from_twitter =soup_twit.find_all("span",text=re.compile('InSight sol'))
    mars_latest_weather = mars_weather_from_twitter[0].get_text()


    import pandas as pd
    facts_url = 'https://space-facts.com/mars/'
    mars_table_df = pd.read_html(facts_url)[0]
    mars_table_df.columns=["Description","Value"]
    mars_table_df.set_index("Description", inplace=True)



    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser4 = init_browser()
    browser4.visit(astro_url)
    astro_html = browser4.html
    astro_soup = bs(astro_html, 'html.parser')

    products = astro_soup.find_all('div', class_='item')

    hemis_dict = {}
    hemisphere_image_urls = []
    for product in products:

        title = product.find('h3').text
        browser4.click_link_by_partial_text(title)
    
        image_url = 'https://astrogeology.usgs.gov' + product.a["href"] 
        browser4.visit(image_url)
        img_html = browser4.html
        img_soup = bs(img_html, 'html.parser')
        image_url =img_soup.find("a", text="Sample")["href"]

        hemis_dict = {'title': title.strip('Enhanced'), 'img_url': image_url}

        hemisphere_image_urls.append(hemis_dict)
        browser4.visit(astro_url)
        astro_html = browser4.html
        astro_soup = bs(astro_html, 'html.parser')


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title.text,
        "news_p": news_p.text,
        "featured_image": featured_image_url,
        "twitter_weather": mars_latest_weather,
        "mars_table" : mars_table_df.to_html(index=True, header=True, border=0),
        "hemisphere_data" : hemisphere_image_urls
    }
    #print(f'mars = {mars_data}')
    print(f'mars = {hemisphere_image_urls[0]["img_url"]}')

    
    # Close the browser after scraping
    browser.quit()
    browser2.quit()
    browser3.quit()
    browser4.quit()

    # Return results
    return mars_data
