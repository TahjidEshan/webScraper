#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
import pandas
import os


def scrapper(driver, lists):

    finalSet = []

    for list in lists:
        driver.get(list)
        valueSet = []
        nameVal = driver.find_element_by_tag_name('h2')
        #print (nameVal.text)
        # sleep(2)
        name = nameVal.text.encode("utf-8")
        valueSet.append(name)
        soup = BeautifulSoup(urlopen(list), "lxml")
        country = soup.findAll('td', attrs={'class': 'label'})

        for element in country:

            if 'Country:' in element.get_text():
                countryName = element.find_next('td')
                # print(countryName.get_text())
                valueSet.append(countryName.get_text().encode("utf-8"))

        emails = set(re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", urlopen(list).read(), re.I))
        email = "   "

        if not emails:
            email = "  "
        else:
            email = emails.pop()

        valueSet.append(email.encode("utf-8"))
        #print (email)
        finalSet.append(valueSet)
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
    return finalSet


def main():
    driver = webdriver.Chrome()
    mainUrl = "https://www.unodc.org/ngo/list.jsp"
    driver.get(mainUrl)
    assert "List" in driver.title
    elems = driver.find_elements_by_xpath("//a[@href]")
    lists = []
    for elem in elems:
        value = elem.get_attribute("href")
        if 'showSingleDetailed' in value:
            lists.append(value)
    finalSet = scrapper(driver, lists)
    finalSet = pandas.DataFrame(finalSet)
    finalSet.columns = ['Name', 'Country', 'Email']
    if not os.path.exists('data.csv'):
        finalSet.to_csv('data.csv', index=False)
    else:
        with open('data.csv', 'a') as f:
            finalSet.to_csv(f, header=False, index=False)
    driver.close()


if __name__ == '__main__':
    main()
