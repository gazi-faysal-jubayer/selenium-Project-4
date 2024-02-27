from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import math
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import pandas as pd

driver = webdriver.Chrome()
#Put your link here
mainlink = "https://mobilityex.com/#/search?svc=Moving%20Services%20Company%20&sort=companylegalname,asc&range=50&mocs=104&assocs=800&query=q%3D%204&spc=10"
driver.get(mainlink)
driver.implicitly_wait(10)

links_list = []
def sub():
    # Find all 'a' tags matching the specific format
    filtered_links = driver.find_elements(By.XPATH, "//a[@ui-sref='searchdetails({id:sp.id})' and @ng-click=\"vm.generateEventGa4('IAMX Profile', {'sp_results_profile': sp.companylegalname, 'sp_legal_name': sp.companylegalname})\" and @analytics-on='click' and @analytics-event='Navigate to Profile Page' and @analytics-label]")

    # Extract the href attribute from each filtered link
    for link in filtered_links:
        href = link.get_attribute('href')
        links_list.append(href)

pages = []
time.sleep(10)
count = int(driver.find_element(By.XPATH, "//*[@id='main']/div/div[2]/jhi-item-count/div").text.split(' ')[-2])
lim = math.ceil(count/30)
for j in range(lim):
# while True:
    try:
        # Find the active page number
        active_page_number = driver.find_element(By.CSS_SELECTOR, "#left > ul > li.pagination-page.active > a").text
        if active_page_number in pages:
            break
        
        print(active_page_number)
        sub()
        
        pages.append(active_page_number)
        
        # # Construct the XPath for the next page
        next_page_xpath = "#left > ul > li.pagination-next > a"

        # # Check if the next page element exists
        next_page_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, next_page_xpath)))

        driver.execute_script("arguments[0].click();", next_page_element)
        time.sleep(3)
        # Wait until the spinner disappears
        # WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, 'sb_loading')))

    except (TimeoutException, StaleElementReferenceException) as e:
        # print(f"Exception: {e}")
        # print(f"Element for page {int(active_page_number) + 1} not found. Exiting the loop.")
        break

    time.sleep(10)

# Close the WebDriver
driver.quit()

# Create a DataFrame from the list of links
df = pd.DataFrame(links_list, columns=['Links'])

# Save the DataFrame to a CSV file
df.to_csv('filtered_links1.csv', index=False) #output file name and directory