# Import BeautifulSoup, Splinter, Chromedriver
from bs4 import BeautifulSoup
from splinter import Browser
from selenium.webdriver.chrome.options import Options
import pandas as pd
import requests
import time

def init_browser():
    #setting up browser parser
    executable_path = {"executable_path": "chromedriver"}
    options=Options()
    options.add_argument('--ignore-certificate-errors')
    browser = Browser("chrome", **executable_path, headless=False,chrome_options=options)
    return browser

# Step 1 - Scraping:
def scrape():
    browser = init_browser()
    # creating data dictionary to fill with all the retrieved data from several websites
    data={}
    # NASA Mars news
    
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    NASA_Mars_news={}
    for item_list in soup.find_all('li',class_='slide'):
        item=item_list.find('div',class_='image_and_description_container')
        news_title=item.find('div', class_='content_title').text
        news_p=item.find('div', class_='article_teaser_body').text
        #print(news_title)
        #print(news_p)
        #print()
        NASA_Mars_news.update({news_title:news_p})
    data.update({'NASA_MARS_NEWS':NASA_Mars_news})

    # JPL Mars Space Images - Featured Image
    #browser = Browser("chrome", **executable_path, headless=False,chrome_options=options)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', {'id':'main_container'}).\
            find('div', {'id':'site_body'}).find('div', {'id':'page'}).\
            find('div', class_='carousel_container')

    url_part=temp.find('article')['style'].split('/',1)[1][:-3]
    featured_image_url="https://www.jpl.nasa.gov/" + url_part

    #print(featured_image_url)
    data.update({'JPL_MARS_SPACE_IMAGE':featured_image_url})

    # Mars Weather
    #browser = Browser("chrome", **executable_path, headless=False,chrome_options=options)
    url='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)  
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather=soup.find('div',{'id':'doc'}).find('div',{'id':'timeline'}).\
            find('div',class_='stream').find('div',class_='content').p.text
    #print(mars_weather)
    data.update({'MARS_WEATHER':mars_weather})

    # Mars Facts: we do NOT need to update the data dictionary for this part
    request_mars_space_facts = requests.get("https://space-facts.com/mars/")
    mars_facts= pd.read_html(request_mars_space_facts.text)[0]
    mars_facts.columns=['Facts', 'values']
    mars_facts.set_index('Facts',inplace=True)
    mars_facts=mars_facts.to_html(index='False',index_names='False')
    data.update({'MARS_FACTS':mars_facts})

    # Mars Hemispheres
    #browser = Browser("chrome", **executable_path, headless=False,chrome_options=options)
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)  
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    base_url='https://astrogeology.usgs.gov/'

    ##  Hemisphere titles
    collapse=soup.find('div', class_='collapsible results')
    hemisphere_titles=[]
    for no,item in enumerate(collapse.find_all('div',class_='item')):
        hemisphere_titles.append(item.a['href'].split('/')[-1])

    ## Hemisphere images
    img_base_url='https://astrogeology.usgs.gov/search/map/Mars/Viking/'
    hemisphere_title_image =[]
    for no,tk in enumerate(hemisphere_titles):
        hem_tit_img={}
        #browser = Browser("chrome", **executable_path, headless=False,chrome_options=options)
        browser.visit(img_base_url+tk)
        time.sleep(5)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hem_tit_img['title']=tk
        hem_tit_img['image']=soup.find('div',class_='container').\
                                    find('div',class_='downloads').ul.li.a['href']
        hemisphere_title_image.append(hem_tit_img)
        
    data.update({'MARS_HEMISPHERES_IMG':hemisphere_title_image})

    # Close the browser after scraping
    browser.quit()

    return (data)

#print(scrape())
