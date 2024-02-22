from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import pandas as pd
import os

columns = [
    'Company Name', 'Address', 'Website', 'Company Description', 'Year Established',
    'Parent Company', 'Contact Name', 'Title', 'Office Phone', 'Email',
    'Association Memberships - FIDI', 'Association Memberships - DAB', 'Association Memberships - Harmony', 'Links'
]
output_file = 'output-3.csv'

# Check if the output file already exists
if not os.path.isfile(output_file):
    empty_df = pd.DataFrame(columns=columns)
    empty_df.to_csv(output_file, index=False)

file_path = 'filtered_links-3.csv'
df = pd.read_csv(file_path)

for c in range(len(df)):
    link = df.iloc[c, 0]
    df1 = pd.read_csv('output-3.csv')
    if link in df1['Links'].values:
        continue  # Skip processing if the link is already in the output
    else:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        # link = 'https://mobilityex.com/#/search/service-providers/597?svc=Moving%20Services%20Company%20&sort=companylegalname,asc&range=50&mocs=104&assocs=800&query=q%3D%204&spc=10'
        driver.get(link)
        driver.implicitly_wait(10)

        comName = driver.find_element(By.XPATH, "//span[@class='label-info col-md-12 col-xs-12']").text
        # print(comName)
        add = driver.find_element(By.XPATH, "//div[@autoscroll='true']//address").text
        # print(add)
        try:
            web = driver.find_element(By.XPATH, "//div[@ng-if='vm.serviceProviders.website']").text
        except NoSuchElementException:
            web = ""
        # print(web)
        disc = driver.find_element(By.XPATH, "//*[@id='view-content']/div[1]/div[2]/div[2]/div[6]/div/p").text
        # print(disc)
        try:
            estYear = driver.find_element(By.XPATH, "//span[@ng-if='vm.serviceProviders.established']").text
        except NoSuchElementException:
            estYear = ""
        # print(estYear)
        try:
            parentCom =  driver.find_element(By.XPATH, "//div[@ng-if='vm.serviceProviders.id != vm.serviceProviders.serviceProvidersId']").text.split(':\n')[1]
        except NoSuchElementException:
            parentCom = ""
        # print(parentCom)


        a = driver.find_element(By.XPATH, "//div[@is-open='status.amopen'] ")
        element = a.find_element(By.CLASS_NAME, "accordion-toggle")
        driver.execute_script("arguments[0].click();", element)
        time.sleep(2)
        assText = driver.find_element(By.XPATH, "//div[@is-open='status.amopen'] ").text
        # print(assText)

        if 'DAB' in assText:
            dab = 'Yes'
        else:
            dab = ''
        if 'FIDI' in assText:
            fidi = 'Yes'
        else:
            fidi = ''
        if 'Harmony' in assText:
            harmony = 'Yes'
        else:
            harmony = ''
            

        x = driver.find_element(By.XPATH, "(//div[@class='panel-body'])")
        y = x.find_elements(By.CLASS_NAME, "col-md-12")
        for i in range(int(len(y)/5)):
            t = y[i*5].text.replace('\n', '').replace('IAM Young Professional', '').split(')')[0]
            try:
                email =  x.find_element(By.XPATH, f"(//div[@ng-if='contact.email'])[{i+1}]").text.replace('\n', '').split(':')[1]
            except NoSuchElementException:
                email = ""
            try:
                phone = x.find_element(By.XPATH, f"(//div[@ng-if='contact.officephone && contact.officephone.length>5'])[{i+1}]").text.replace('\n', '').split(':')[1]
            except NoSuchElementException:
                phone = ""
            title = t.split('(')[1]
            name = t.split('(')[0]
            
            data = {
                'Company Name': comName,
                'Address': add,
                'Website': web,
                'Company Description': disc,
                'Year Established': estYear,
                'Parent Company': parentCom,
                'Contact Name': name,
                'Title': title,
                'Office Phone': phone,
                'Email': email,
                'Association Memberships - FIDI': fidi,
                'Association Memberships - DAB': dab,
                'Association Memberships - Harmony': harmony,
                'Links': link,
            }
            # print(data)
            data_list = [data]
            existing_data = pd.read_csv('output-3.csv')
            new_data_df = pd.DataFrame(data_list, columns=columns)
            updated_data = existing_data._append(new_data_df, ignore_index=True)
            updated_data.to_csv('output-3.csv', index=False)
            
        driver.quit()

