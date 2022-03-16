import time
import os
import pandas as pd
from selenium import webdriver
from matplotlib.pyplot import text
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

#initiate the clock to estimate the code execution time.
t0 = time.time()
'''
Some scholars have a long list of publications, and user need to click on 'Show More' button
to render the entire page. Below, please enter the minimum number of clicks required to render the entire
page for a given scholar.
'''
clicks = 4

'''
Enter the minimim number of papers that you expect the author has in his profile.
'''
papers = 100


#Enter the url to the Profile of a Scholar on Google Scholar.
# Multiple urls can be entered separated by a comma 
url = [
    "https://scholar.google.ca/citations?user=XwdIvRYAAAAJ&hl=en",
    "https://scholar.google.ca/citations?hl=en&user=qGUo2OYAAAAJ"
]

# Open the browser and the url.
for index in url:
    driver = webdriver.Chrome()
    print('Opening Browser')
    driver.get(index)
    print('Browser opened the requested url')
    time.sleep(0.3)   
    button = driver.find_element_by_xpath('//*[@id="gsc_bpf_more"]')
    
    #click on 'Show More' button
    no_of_clicks = clicks
    while no_of_clicks > 1:
        button.click()
        print('click-',{no_of_clicks})
        no_of_clicks -= 1
        time.sleep(1)
    
    body = driver.find_element_by_tag_name('body')
    scholar_name = body.find_element_by_xpath('//*[@id="gsc_prf_in"]').text
    manuscripts = []
    journal = []
    author_list = []
    citations = []
    publication_year = []

    no_of_papers = papers
    for index in range(0,no_of_papers):
        try:
            print(index)
            manuscripts_iter = (body.find_elements_by_class_name('gsc_a_at'))[index].text
            journal_iter = (body.find_elements_by_class_name('gs_gray'))[2*index+1].text
            author_list_iter = (body.find_elements_by_class_name('gs_gray'))[2*index].text
            citations_iter = (body.find_elements_by_class_name('gsc_a_ac.gs_ibl'))[index].text
            publication_year_iter = (body.find_elements_by_class_name('gsc_a_h.gsc_a_hc.gs_ibl'))[index].text
            manuscripts.append(manuscripts_iter)
            journal.append(journal_iter)
            author_list.append(author_list_iter)
            citations.append(citations_iter)
            publication_year.append(publication_year_iter)
        except IndexError:
            pass
        continue

    # Save the scraped information into a dataframe.
    data = pd.DataFrame({
        'manuscript_title' : manuscripts,
        'authors' : author_list,
        'journal_name' :  journal,
        'no_of_citations' : citations,
        'year_of_publication' : publication_year
        
    })
    print(data)
    driver.quit()

    #Save .xlsx file in you current working directory.
    path = os.getcwd()+f'/scholar_name_{scholar_name}.xlsx'
    data.to_excel(excel_writer= path, index = False)
    driver.quit()

execution_time = time.time()-t0
print('The code execution time (in seconds) is', execution_time)
print('Code execution completed.')