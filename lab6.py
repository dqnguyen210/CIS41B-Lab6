#lab6: Accessing the web and going back to the basics
#Name: Quynh Nguyen
#Date: 2/25/18

'''
In order to get data, I first access the website to store the list of countries and their URLs.
The data is stored in a dictionary of list, where the key is the first character of the country name
and value is a sorted list of tuple (country name, URL). Once the user chooses which country to display,
the program goes to the country's URL and prints out the table of information. Since the data just needs
to be printed without being analyzed, it will not be stored to save memory. However, because printing data 
requires the program to go to the link, fetch data and parse the string, it takes a while to see data on screen.
'''

import requests
from bs4 import BeautifulSoup 
from collections import defaultdict
import re
import time

def getCountryList() :
    '''Fuction fetch data from the website and store data in a dictionary, with
       key=first letter of name, value= sorted list of countries and the URLs to the info table
    '''
    page = requests.get("https://www.olympic.org/pyeongchang-2018/results/en/general/nocs-list.htm")
    soup = BeautifulSoup(page.content, 'lxml')
    baseLink = "https://www.olympic.org/pyeongchang-2018/results/"

    countryDict = defaultdict(list)
    for country in soup.find_all('div', class_='CountriesListItem') :
        name = country.find('strong').get_text()
        url = re.sub('../../', baseLink, country.find('a').get('href'))
        countryDict[name[0]].append((name, url))
        countryDict[name[0]].sort()
    return countryDict
    
def printCountryInfo(url) :
    '''Fetch data from the URL and print the info table of the country
    '''
    #start = time.time()    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')    
    
    table = soup.find('table', class_='ResTableFull')
    for row in table.find_all('tr') : 
        # use regex to parse data from the string
        texts = re.findall("[\w\-? *]+", row.get_text())
        print('%30s %6s %6s %9s' %(texts[0], texts[1], texts[2], texts[3]))
    #print(time.time() - start)

    
def main():
    dataDict = getCountryList()
    letter = 'a'
    while letter != '0':
        invalid = True # flag for invalid input
        try:
            letter = input("\nEnter the first letter of country name or 0 to exit: ").upper()            
            if not letter.isalpha() :
                raise ValueError("=> Invalid letter of the alphabet")
            if letter not in dataDict : 
                raise ValueError("=> No country name matching the letter")
            
            #print the list of countries starting with the letter
            print("Countries participating in the Winter Olympics: ")
            for i,country in enumerate(dataDict[letter]) :                
                print("\t\t%d: %s" %(i+1, country[0]))
            
            while (invalid) : # re-prompt when invalid input
                option = input("\nType in a number: ")
                if not (option.isdigit() and 1 <= int(option) <= len(dataDict[letter])):
                    print("=> Invalid number chosen from the country list")
                else:
                    option = int(option)
                    print("Data for %s:" %dataDict[letter][option-1][0]) # print country name
                    printCountryInfo(dataDict[letter][option-1][1])      # go to the link to print data
                    invalid = False 
                  
        except ValueError as e:
            print(e)
    print("\nThank you for using the program!")
    
    
main()
