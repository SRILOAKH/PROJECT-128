from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
import csv
from attr import define
import requests

START_URL="https://en.wikipedia.org/wiki/List_of_brown_dwarfs/"
browser=webdriver.Chrome("/Users/M V R CHOWDHARY/OneDrive/Desktop/PYTHON/chromedriver")
browser.get(START_URL)
time.sleep(10)
def scrape():
    headers=["name","distance","mass","radius",]
    stars_data=[]
    for i in range(0, 428): 
        soup = BeautifulSoup(browser.page_source, "html.parser")
        current_page_num = int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value")) 
        if current_page_num < i: 
            browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click() 
        elif current_page_num > i: 
            browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click() 
        else: break
         
        for ul_tag in soup.find_all("ul", attrs={"class", "stars"}): 
            li_tags = ul_tag.find_all("li") 
            temp_list = []
            for index, li_tag in enumerate(li_tags): 
                if index == 0: 
                    temp_list.append(li_tag.find_all("a")[0].contents[0]) 
                else: 
                    try: 
                        temp_list.append(li_tag.contents[0]) 
                    except: 
                        temp_list.append("") 
                        hyperlink_li_tag=li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov"+ hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            stars_data.append(temp_list)
            browser.find_element(By.XPATH,'//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click() 
scrape() 
new_stars_data = [] 
def scrape_more_data(hyperlink): 
    try: 
        page = requests.get(hyperlink) 
        soup = BeautifulSoup(page.content, "html.parser") 
        temp_list = [] 
        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}): 
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags: 
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0]) 
                except:
                 temp_list.append("") 
            new_stars_data.append(temp_list) 
    except: 
        time.sleep(1) 
        scrape_more_data(hyperlink) #Calling method
for index, data in enumerate(new_stars_data): 
    scrape_more_data(data[5]) 
    print(f"scraping at hyperlink {index+1} is completed.") 
print(new_stars_data[0:10]) 
final_planet_data = []
for index, data in enumerate(new_stars_data): 
    new_stars_data_element = new_stars_data[index] 
    new_stars_data_element = [elem.replace("\n", "") for elem in new_stars_data_element] 
    new_stars_data_element = new_stars_data_element[:7] 
    new_stars_data.append(data + new_stars_data_element)
    with open("scrapper_2.csv", "w") as f: 
        csvwriter = csv.writer(f) 
        csvwriter.writerow(headers) 
        csvwriter.writerows(new_stars_data) 
scrape()

